from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.model_schemas import TrainingConfig, TrainingResponse
from models.model_metadata import ModelMetadata
from core.training import get_trainer
from core.config import settings
import pandas as pd
import uuid
import os

router = APIRouter(prefix="/models", tags=["Model Training"])

def run_training_job(job_id: str, config: dict, db: str):
    with Session(get_db()) as session:
        try:
            # Load dataset
            df = pd.read_csv(os.path.join(settings.data_dir, db))
            X = df.drop(columns=[config['target_column']])
            y = df[config['target_column']]
            # Initialize and train model
            trainer = get_trainer(config)
            trainer.train(X, y)
            metrics = trainer.evaluate(X, y)
            model_path = trainer.save_model(job_id)
            # Update metadata
            session.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).update({
                'status': 'completed',
                'metrics': metrics,
                'model_path': model_path
            })
            session.commit()
        except Exception as e:
            session.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).update({
                'status': f'failed: {str(e)}'
            })
            session.commit()

@router.post("/train", response_model=TrainingResponse)
async def train_model(
    config: TrainingConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job_id = str(uuid.uuid4())
    db_model = ModelMetadata(
        job_id=job_id,
        algorithm=config.algorithm,
        status='pending',
        parameters=config.dict()
    )
    db.add(db_model)
    db.commit()
    
    background_tasks.add_task(run_training_job, job_id, config.dict(), db)
    return {
        "job_id": job_id,
        "status": "training_started"
    }

@router.get("/{job_id}", response_model=TrainingResponse)
async def get_training_status(job_id: str, db: Session = Depends(get_db)):
    model = db.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Training job not found")
    return model