from __future__ import annotations

"""Utilities for configuring and instantiating model handlers.

The goal of this module is to make it trivial to add new models to the
server application. ``BasicModelHandler`` covers the common life cycle
of a model: build, train, predict, load, save and export so it can later
be served from Triton. New models only need to subclass
:class:`BasicModelHandler` and register themselves with
:func:`register_model`.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

import matplotlib.pyplot as plt
import torch
from torchvision import transforms as T
from torchmetrics import Accuracy, JaccardIndex, F1Score, MetricCollection

try:  # segmentation models provides additional useful metrics
    from segmentation_models_pytorch.utils.metrics import (
        Accuracy as SMPAccuracy,
        Fscore as SMPFscore,
        IoU as SMPIoU,
    )
except Exception:  # pragma: no cover - optional dependency
    SMPAccuracy = SMPFscore = SMPIoU = None

try:  # ``segmentation_models_pytorch`` is optional
    import segmentation_models_pytorch as smp
except Exception:  # pragma: no cover - optional dependency
    smp = None

from jinja2 import Template

CONFIG_TPL = """
    name: "{{ name }}"
    platform: "{{ platform }}"
    max_batch_size: {{ max_batch_size }}
    {% if dynamic_batching %}
    dynamic_batching {{ dynamic_batching }}
    {% endif %}
    input [
    {% for inp in inputs %}
    {
        name: "{{ inp.name }}"
        data_type: {{ inp.data_type }}
        dims: [ {{ inp.dims | join(", ") }} ]
    }
    {% endfor %}
    ]
    output [
    {% for out in outputs %}
    {
        name: "{{ out.name }}"
        data_type: {{ out.data_type }}
        dims: [ {{ out.dims | join(", ") }} ]
    }
    {% endfor %}
    ]
    """


class BasicModelHandler(ABC):
    """Abstract base class for model configuration.

    The idea is that every model handler exposes a minimal API so it can
    be used for training, inference and deployment.  Subclasses only need
    to implement the abstract methods below.  In addition to the usual
    ``build``/``train``/``predict`` cycle, a handler may provide
    ``preprocess`` and ``postprocess`` hooks so data preparation logic can
    be neatly encapsulated.  ``evaluate`` can be implemented to compute
    metrics over a dataset and ``plot_metrics`` may visualise them.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def build(self) -> None:
        """Create and configure the model."""

    @abstractmethod
    def train(self, data: Any) -> None:
        """Train the model with the provided data."""

    @abstractmethod
    def predict(self, inputs: Any) -> Any:
        """Run inference and return model predictions."""

    # ------------------------------------------------------------------
    # Optional processing and evaluation hooks
    # ------------------------------------------------------------------

    def preprocess(self, inputs: Any) -> Any:
        """Pre-process raw inputs before feeding them to the model."""
        return inputs

    def postprocess(self, outputs: Any) -> Any:
        """Post-process model outputs before returning them."""
        return outputs

    def evaluate(self, data: Any) -> Dict[str, float]:  # pragma: no cover - optional
        """Evaluate the model and return a dictionary of metrics."""
        raise NotImplementedError

    def plot_metrics(self, metrics: Dict[str, float], output_path: str) -> None:
        """Visualize metrics and store the figure at ``output_path``."""
        raise NotImplementedError

    # @abstractmethod
    # def export_for_triton(self, output_path: str) -> None:
    #     """Export the model so it can be served from Triton."""

    def export_for_triton(self, output_path: str):
        # 1. Carpeta versión
        model_dir = os.path.join(output_path, self.name, "1")
        os.makedirs(model_dir, exist_ok=True)

        # 2. Export ONNX / TensorRT según backend
        dummy = torch.randn(*self.config["export_input_shape"])
        if self.config["backend"] == "onnx":
            onnx_file = os.path.join(model_dir, "model.onnx")
            torch.onnx.export(self.model, dummy, onnx_file, **self.config.get("onnx_export_args", {}))
        elif self.config["backend"] == "tensorrt":
            # aquí pondrías tu lógica de TensorRT plan export
            plan_file = os.path.join(model_dir, "model.plan")
            self._export_trt(dummy, plan_file)
        else:
            raise ValueError("Backend no soportado")

        # 3. Renderizar plantilla
        tpl = Template(CONFIG_TPL)
        pbtxt = tpl.render(
            name=self.name,
            platform=self.config["triton_platform"],
            max_batch_size=self.config.get("max_batch_size", 1),
            dynamic_batching=self.config.get("dynamic_batching", None),
            inputs=self.config["inputs"],   # lista de dicts con name, data_type, dims
            outputs=self.config["outputs"], # idem
        )

        # 4. Guardar config.pbtxt
        with open(os.path.join(model_dir, "config.pbtxt"), "w") as f:
            f.write(pbtxt)

    @abstractmethod
    def load(self, model_path: str) -> None:
        """Load model weights from ``model_path`` for re-training."""

    @abstractmethod
    def save(self, model_path: str) -> None:
        """Save the model weights to ``model_path`` in PyTorch format."""


_MODEL_REGISTRY: Dict[str, Type[BasicModelHandler]] = {}


def register_model(name: str) -> Any:
    """Class decorator to register new model handlers."""

    def decorator(cls: Type[BasicModelHandler]) -> Type[BasicModelHandler]:
        _MODEL_REGISTRY[name] = cls
        return cls

    return decorator


def create_model_handler(name: str, config: Dict[str, Any]) -> BasicModelHandler:
    """Factory function that instantiates the requested model handler."""

    if name not in _MODEL_REGISTRY:
        raise ValueError(f"Unknown model handler: {name}")
    return _MODEL_REGISTRY[name](config)


@register_model("segmentation")
class SegmentationModelHandler(BasicModelHandler):
    """Example implementation for a segmentation task."""

    def build(self) -> None:
        """Create a segmentation model using ``segmentation_models_pytorch``."""
        if smp is None:
            raise RuntimeError(
                "segmentation_models_pytorch is required for this handler"
            )

        arch = self.config.get("architecture", "Unet")
        encoder = self.config.get("encoder", "resnet34")
        n_classes = int(self.config.get("num_classes", 1))

        try:
            model_class = getattr(smp, arch)
        except AttributeError as exc:
            raise ValueError(f"Unknown segmentation architecture: {arch}") from exc

        self.model = model_class(encoder_name=encoder, classes=n_classes)

    # Data processing ---------------------------------------------------

    def preprocess(self, inputs: Any) -> Any:
        """Convert PIL images to normalized tensors."""
        if isinstance(inputs, torch.Tensor):
            return inputs
        transform = T.Compose([
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        return transform(inputs).unsqueeze(0)

    def postprocess(self, outputs: Any) -> Any:
        """Return the predicted mask index."""
        if isinstance(outputs, torch.Tensor):
            return torch.argmax(outputs, dim=1)
        return outputs

    # ------------------------------------------------------------------
    # Training and inference
    # ------------------------------------------------------------------

    def train(self, data: Any) -> None:
        """Tiny training loop placeholder."""
        if not hasattr(self, "model"):
            self.build()

        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters())
        for images, masks in data:  # ``data`` should be a DataLoader
            optimizer.zero_grad()
            preds = self.model(images)
            loss = torch.nn.functional.cross_entropy(preds, masks)
            loss.backward()
            optimizer.step()

    def predict(self, inputs: Any) -> Any:
        """Run inference on a batch of images."""
        if not hasattr(self, "model"):
            self.build()

        self.model.eval()
        with torch.no_grad():
            return torch.softmax(self.model(inputs), dim=1)

    def evaluate(self, data: Any) -> Dict[str, float]:
        """Compute accuracy, IoU and F1 metrics over ``data``."""
        if not hasattr(self, "model"):
            self.build()

        self.model.eval()
        n_classes = int(self.config.get("num_classes", 1))
        metrics = MetricCollection(
            {
                "accuracy": Accuracy(task="multiclass", num_classes=n_classes),
                "iou": JaccardIndex(task="multiclass", num_classes=n_classes),
                "f1": F1Score(task="multiclass", num_classes=n_classes),
            }
        )

        # metrics provided by segmentation_models_pytorch
        smp_metrics = {}
        if SMPIoU is not None:
            smp_metrics["iou_smp"] = SMPIoU()
        if SMPFscore is not None:
            smp_metrics["f1_smp"] = SMPFscore()
        if SMPAccuracy is not None:
            smp_metrics["accuracy_smp"] = SMPAccuracy()

        with torch.no_grad():
            for images, masks in data:
                preds = self.postprocess(self.predict(images))
                metrics.update(preds, masks)
                for m in smp_metrics.values():
                    m.update(preds, masks)
        computed = {key: float(val) for key, val in metrics.compute().items()}
        for name, m in smp_metrics.items():
            computed[name] = float(m.compute())
        return computed

    def plot_metrics(self, metrics: Dict[str, float], output_path: str) -> None:
        """Create a simple bar plot with the provided metrics."""
        fig = plt.figure()
        plt.bar(list(metrics.keys()), list(metrics.values()))
        plt.ylabel("score")
        plt.tight_layout()
        fig.savefig(output_path)

    def export_for_triton(self, output_path: str) -> None:
        """Export the model to ONNX format for Triton."""
        if not hasattr(self, "model"):
            self.build()

        dummy = torch.randn(1, 3, 224, 224)
        torch.onnx.export(self.model, dummy, output_path)

    def load(self, model_path: str) -> None:
        """Load model weights from ``model_path``."""
        if not hasattr(self, "model"):
            self.build()

        state = torch.load(model_path, map_location="cpu")
        self.model.load_state_dict(state)

    def save(self, model_path: str) -> None:
        """Save model weights in PyTorch format."""
        if not hasattr(self, "model"):
            self.build()

        torch.save(self.model.state_dict(), model_path)