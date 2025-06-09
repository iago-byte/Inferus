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

import torch

try:  # ``segmentation_models_pytorch`` is optional
    import segmentation_models_pytorch as smp
except Exception:  # pragma: no cover - optional dependency
    smp = None


class BasicModelHandler(ABC):
    """Abstract base class for model configuration.

    The idea is that every model handler exposes a minimal API so it can
    be used for training, inference and deployment.  Subclasses only need
    to implement the abstract methods below.
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

    @abstractmethod
    def export_for_triton(self, output_path: str) -> None:
        """Export the model so it can be served from Triton."""

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
