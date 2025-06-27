from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from service import ModelService, load_model, unload_model
from task_worker import status, shutdown

app = FastAPI(title="Inferus API")
service = ModelService()

class TrainRequest(BaseModel):
    name: str
    model_type: str
    config: dict  # hiperparámetros, MLflow + export settings

class ExportRequest(BaseModel):
    name: str
    output_path: str
    # Opcionales para Triton
    # backend: str  # "onnx" o "tensorrt"
    # triton_params: dict

class DeployRequest(BaseModel):
    name: str
    model_path: str

@app.post("/train")
async def train(req: TrainRequest):
    if service.exists(req.name):
        raise HTTPException(status_code=400, detail="Model name already registered")
    task_id = service.train(req.name, req.model_type, req.config)
    return {"task_id": task_id, "status": "queued"}

@app.post("/export")
async def export_model(req: ExportRequest):
    if not service.exists(req.name):
        raise HTTPException(status_code=404, detail="Model not found")
    task_id = service.export(req.name, req.output_path)
    return {"task_id": task_id, "status": "queued"}

@app.post("/deploy")
async def deploy(req: DeployRequest):
    if not service.exists(req.name):
        raise HTTPException(status_code=404, detail="Model not found")
    # Cargamos el handler interno y registramos con Triton
    task_id = service.deploy(req.name, req.model_path)
    # Tras completar export, invocamos a Triton
    # Si usas modo explicit, carga manualmente
    load_model(req.name)
    return {"task_id": task_id, "status": "queued"}

@app.post("/unload/{name}")
async def unload(name: str):
    if not service.exists(name):
        raise HTTPException(status_code=404, detail="Model not found")
    unload_model(name)
    return {"status": "unloaded", "name": name}

@app.post("/infer")
async def infer(name: str, image: UploadFile = File(...)):
    if not service.exists(name):
        raise HTTPException(status_code=404, detail="Model not found")
    data = await image.read()
    task_id = service.infer(name, data)
    return {"task_id": task_id, "status": "queued"}

@app.get("/tasks/{task_id}")
def get_status(task_id: str):
    return status(task_id)

@app.get("/models")
def list_models():
    return {"available_models": service.list()}

@app.on_event("shutdown")
def on_shutdown():
    shutdown()
