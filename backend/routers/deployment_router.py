from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.model_metadata import ModelMetadata
from core.config import settings
import os
import shutil
from core.security import get_current_active_user

router = APIRouter(prefix="/deployment", tags=["Deployment"], dependencies=[Depends(get_current_active_user)])

@router.post("/deploy/{job_id}")
async def deploy_model(job_id: str, db: Session = Depends(get_db)):
    model_metadata = db.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).first()
    if not model_metadata:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Deployment logic here
        return {"message": f"Model {job_id} deployed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))