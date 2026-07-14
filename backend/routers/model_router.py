from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.model_schemas import TrainingConfig, TrainingResponse
from models.model_metadata import ModelMetadata
from core.training import get_trainer
from core.config import settings
from core.cloud_storage import S3Client
import pandas as pd
import uuid
import os

router = APIRouter(prefix="/models", tags=["Model Training"])

def run_training_job(job_id: str, config: dict, dataset_path: str, db: Session):
    try:
        # Load dataset
        s3_client = S3Client()
        local_dataset_path = f"{settings.data_dir}/{os.path.basename(dataset_path)}"
        s3_client.download_file(dataset_path, local_dataset_path)

        df = pd.read_csv(local_dataset_path)
        X = df.drop(columns=[config['target_column']])
        y = df[config['target_column']]

        # Initialize and train model
        trainer = get_trainer(config['algorithm'], config)
        trainer.train(X, y)
        metrics = trainer.evaluate(X, y)

        # Save model to local and upload to S3
        local_model_path = trainer.save_model()
        s3_model_path = s3_client.upload_file(local_model_path, f"models/{job_id}.pkl")

        # Save metadata to database
        model_metadata = ModelMetadata(
            job_id=job_id,
            algorithm=config['algorithm'],
            parameters=config['params'],
            metrics=metrics,
            status="completed",
            model_path=s3_model_path
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
    job_id = str(uuid.uuid4())
    dataset_metadata = db.query(DatasetMetadata).filter(DatasetMetadata.id == config.dataset_id).first()
    if not dataset_metadata:
        raise HTTPException(status_code=404, detail="Dataset not found")

    background_tasks.add_task(run_training_job, job_id, config.dict(), dataset_metadata.connection_string, db)

    return TrainingResponse(
        job_id=job_id,
        status="started"
    )
