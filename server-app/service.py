from typing import Any, Dict, List
import io
import torch
from PIL import Image
from torchvision import transforms
import mlflow
import mlflow.pytorch
from model_handler import create_model_handler
from task_worker import submit

# Registro en memoria de handlers activos
t:
handlers: Dict[str, Any] = {}

# ------------------ Definición de tareas en background ------------------

def _train_task(name: str, model_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    # 1) MLflow: iniciar experimento y logging de parámetros
    mlflow.set_tracking_uri(config.get("mlflow_tracking_uri", "http://mlflow:5000"))
    mlflow.set_experiment(config.get("mlflow_experiment_name", "inferus_experiments"))
    with mlflow.start_run(run_name=name):
        mlflow.log_params({"model_type": model_type, **config.get("mlflow_params", {})})
        # 2) Crear handler y entrenar
        handler = create_model_handler(model_type, config)
        dataset = config.get("train_data")
        if dataset is None:
            # Dataset dummy por defecto
            input_shape = config.get("input_shape", (1, 3, 224, 224))
            dummy = (torch.randn(*input_shape),
                     torch.zeros(input_shape[0], *input_shape[2:], dtype=torch.long))
            handler.train([dummy])
        else:
            handler.train(dataset)
        # 3) Registrar métricas opcionales\ n        for m, v in config.get("mlflow_metrics", {}).items():
            mlflow.log_metric(m, v)
        # 4) Registrar modelo PyTorch en MLflow
        mlflow.pytorch.log_model(handler.model, artifact_path="pytorch_model")
    # 5) Guardar handler en memoria para posteriores export/deploy/infer
    handlers[name] = handler
    return {"status": "trained", "name": name}


def _export_task(name: str, output_path: str) -> Dict[str, Any]:
    handler = handlers.get(name)
    if handler is None:
        raise RuntimeError(f"Model '{name}' not found")
    # Exporta la carpeta con versión y config.pbtxt dinámica
    handler.export_for_triton(output_path)
    return {"status": "exported", "name": name, "path": output_path}


def _deploy_task(name: str, model_path: str) -> Dict[str, Any]:
    handler = handlers.get(name)
    if handler is None:
        raise RuntimeError(f"Model '{name}' not found")
    handler.load(model_path)
    return {"status": "deployed", "name": name}


def _infer_task(name: str, data: bytes) -> Dict[str, Any]:
    handler = handlers.get(name)
    if handler is None:
        raise RuntimeError(f"Model '{name}' not found")
    # Preprocesado de imagen
    image = Image.open(io.BytesIO(data)).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize(handler.config.get("input_resize", (224, 224))),
        transforms.ToTensor(),
    ])
    tensor = transform(image).unsqueeze(0)
    preds = handler.predict(tensor)
    return {"predictions": preds.argmax(dim=1).tolist()}


# ------------------ Servicio de alto nivel ------------------

class ModelService:
    def exists(self, name: str) -> bool:
        return name in handlers

    def list(self) -> List[str]:
        return list(handlers.keys())

    def train(self, name: str, model_type: str, config: Dict[str, Any]) -> str:
        """Encola la tarea de entrenamiento y devuelve su ID."""
        return submit(_train_task, name, model_type, config)

    def export(self, name: str, output_path: str) -> str:
        """Encola la tarea de export para Triton y devuelve su ID."""
        return submit(_export_task, name, output_path)

    def deploy(self, name: str, model_path: str) -> str:
        """Encola la carga del modelo en memoria y devuelve su ID."""
        return submit(_deploy_task, name, model_path)

    def infer(self, name: str, data: bytes) -> str:
        """Encola la tarea de inferencia y devuelve su ID."""
        return submit(_infer_task, name, data)
