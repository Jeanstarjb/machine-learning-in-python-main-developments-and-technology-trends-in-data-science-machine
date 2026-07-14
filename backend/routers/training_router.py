from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.model_metadata import ModelMetadata
from schemas.model_schemas import TrainingConfig, TrainingResponse
from core.training import get_trainer
from core.config import settings
import pandas as pd
import uuid
import os

router = APIRouter(prefix="/training", tags=["Training"])

def run_training_job(job_id: str, config: dict, dataset_path: str, db: Session):
    try:
        # Load dataset
        df = pd.read_csv(dataset_path)
        X = df.drop(columns=[config['target_column']])
        y = df[config['target_column']]

        # Initialize and train model
        trainer = get_trainer(config['algorithm'], config)
        trainer.train(X, y)

        # Evaluate model
        metrics = trainer.evaluate(X, y)

        # Save model
        model_path = os.path.join(settings.model_dir, f"{job_id}.pkl")
        trainer.save_model(model_path)

        # Update database
        model_metadata = ModelMetadata(
            job_id=job_id,
            algorithm=config['algorithm'],
            parameters=config,
            metrics=metrics,
            status="completed",
            model_path=model_path
        )
        db.add(model_metadata)
        db.commit()
    except Exception as e:
        model_metadata = db.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).first()
        if model_metadata:
            model_metadata.status = "failed"
            db.commit()
        raise e

@router.post("/train", response_model=TrainingResponse)
async def train_model(
    config: TrainingConfig,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Validate dataset
    dataset_path = os.path.join(settings.data_dir, config.dataset_name)
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Generate job ID
    job_id = str(uuid.uuid4())

    # Save job metadata
    model_metadata = ModelMetadata(
        job_id=job_id,
        algorithm=config.algorithm,
        parameters=config.dict(),
        status="in_progress"
    )
    db.add(model_metadata)
    db.commit()

    # Run training in background
    background_tasks.add_task(run_training_job, job_id, config.dict(), dataset_path, db)

    return TrainingResponse(job_id=job_id, status="in_progress")