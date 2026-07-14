from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from core.evaluation.metrics import EvaluationMetrics
from core.evaluation.visualization import EvaluationVisualization
from database.session import get_db
from models.model_metadata import ModelMetadata
from core.config import settings
import pandas as pd
import os
import numpy as np

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.post("/evaluate/{job_id}")
async def evaluate_model(job_id: str, db: Session = Depends(get_db)):
    # Fetch model metadata
    model_metadata = db.query(ModelMetadata).filter(ModelMetadata.job_id == job_id).first()
    if not model_metadata:
        raise HTTPException(status_code=404, detail="Model not found")

    # Load model
    model_path = model_metadata.model_path
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model file not found")

    model = joblib.load(model_path)

    # Load dataset
    dataset_path = os.path.join(settings.data_dir, model_metadata.parameters['dataset_name'])
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pd.read_csv(dataset_path)
    X = df.drop(columns=[model_metadata.parameters['target_column']])
    y = df[model_metadata.parameters['target_column']]

    # Evaluate model
    predictions = model.predict(X)
    y_proba = None
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X)

    metrics = EvaluationMetrics.calculate_classification_metrics(y, predictions, y_proba)

    # Save metrics to database
    model_metadata.metrics = metrics
    db.commit()

    # Generate and save visualizations
    cm = metrics["confusion_matrix"]
    class_names = list(df[model_metadata.parameters['target_column']].unique())
    cm_path = os.path.join(settings.model_dir, f"{job_id}_confusion_matrix.png")
    EvaluationVisualization.plot_confusion_matrix(np.array(cm), class_names, cm_path)

    return {"job_id": job_id, "metrics": metrics, "confusion_matrix_path": cm_path}