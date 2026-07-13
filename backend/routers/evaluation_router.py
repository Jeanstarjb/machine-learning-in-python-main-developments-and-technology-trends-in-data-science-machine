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

    # Load model and dataset
    model_path = model_metadata.model_path
    dataset_path = os.path.join(settings.data_dir, model_metadata.parameters['dataset_name'])
    if not os.path.exists(model_path) or not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Model or dataset not found")

    model = joblib.load(model_path)
    df = pd.read_csv(dataset_path)

    X = df.drop(columns=[model_metadata.parameters['target_column']])
    y_true = df[model_metadata.parameters['target_column']]

    # Generate predictions
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else None

    # Calculate metrics
    if model_metadata.parameters['problem_type'] == 'classification':
        metrics = EvaluationMetrics.calculate_classification_metrics(y_true, y_pred, y_proba)
        cm_path = os.path.join(settings.model_dir, f"{job_id}_confusion_matrix.png")
        EvaluationVisualization.plot_confusion_matrix(np.array(metrics['confusion_matrix']), model.classes_, cm_path)
        metrics['confusion_matrix_plot'] = cm_path
    else:
        metrics = EvaluationMetrics.calculate_regression_metrics(y_true, y_pred)

    # Update model metadata with evaluation results
    model_metadata.metrics = metrics
    db.commit()

    return {"job_id": job_id, "metrics": metrics}