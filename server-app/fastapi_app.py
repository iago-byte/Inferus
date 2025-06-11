from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import torch
from model_handler import create_model_handler
from task_worker import submit, status

app = FastAPI(title="Inferus API")
handlers = {}  # model_name -> handler instance

class TrainRequest(BaseModel):
    name: str
    model_type: str
    config: dict

class DeployRequest(BaseModel):
    name: str
    model_path: str

class ExportRequest(BaseModel):
    name: str
    output_path: str

# ---------------- Background Task Functions ----------------
def _train_task(req: TrainRequest) -> dict:
    handler = create_model_handler(req.model_type, req.config)
    dummy = [(torch.randn(1, 3, 224, 224), torch.zeros(1, 224, 224, dtype=torch.long))]
    handler.train(dummy)
    handlers[req.name] = handler
    return {"status": "trained", "name": req.name}

def _export_task(req: ExportRequest) -> dict:
    handler = handlers.get(req.name)
    if handler is None:
        raise RuntimeError("Model not found")
    handler.export_for_triton(req.output_path)
    return {"status": "exported", "path": req.output_path}

def _deploy_task(req: DeployRequest) -> dict:
    handler = handlers.get(req.name)
    if handler is None:
        raise RuntimeError("Model not found")
    handler.load(req.model_path)
    return {"status": "deployed", "name": req.name}

def preprocess_image(data: bytes) -> torch.Tensor:
    from PIL import Image
    import io
    from torchvision import transforms
    image = Image.open(io.BytesIO(data)).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    return transform(image).unsqueeze(0)

def _infer_task(name: str, data: bytes) -> dict:
    handler = handlers.get(name)
    if handler is None:
        raise RuntimeError("Model not found")
    tensor = preprocess_image(data)
    preds = handler.predict(tensor)
    return {"predictions": preds.argmax(dim=1).tolist()}

# ---------------- API Endpoints ----------------
@app.post("/train")
async def train(req: TrainRequest):
    task_id = submit(_train_task, req)
    return {"task_id": task_id, "status": "queued"}

@app.post("/export")
async def export_model(req: ExportRequest):
    if req.name not in handlers:
        raise HTTPException(status_code=404, detail="Model not found")
    task_id = submit(_export_task, req)
    return {"task_id": task_id, "status": "queued"}

@app.post("/deploy")
async def deploy(req: DeployRequest):
    if req.name not in handlers:
        raise HTTPException(status_code=404, detail="Model not found")
    task_id = submit(_deploy_task, req)
    return {"task_id": task_id, "status": "queued"}

@app.post("/infer")
async def infer(name: str, image: UploadFile = File(...)):
    if name not in handlers:
        raise HTTPException(status_code=404, detail="Model not found")
    data = await image.read()
    task_id = submit(_infer_task, name, data)
    return {"task_id": task_id, "status": "queued"}

@app.get("/tasks/{task_id}")
async def get_status(task_id: str):
    return status(task_id)

@app.get("/models")
def list_models():
    return {"available_models": list(handlers.keys())}