from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.model_metadata import ModelMetadata
from core.config import settings
import os
import shutil

router = APIRouter(prefix="/deployment", tags=["Deployment"])

@router.post("/deploy/{job_id}")
async def deploy_model(job_id: str, db: Session = Depends(get_db)):
    # Fetch model metadata
    model_metadata = db.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).first()
    if not model_metadata:
        raise HTTPException(status_code=404, detail="Model not found")

    # Check if model file exists
    model_path = model_metadata.model_path
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found")

    # Deploy model (for simplicity, copy to a deployment directory)
    deployment_dir = os.path.join(settings.model_dir, "deployed")
    os.makedirs(deployment_dir, exist_ok=True)
    deployed_model_path = os.path.join(deployment_dir, f"{job_id}.pkl")
    shutil.copy(model_path, deployed_model_path)

    return {"job_id": job_id, "status": "deployed", "deployed_model_path": deployed_model_path}