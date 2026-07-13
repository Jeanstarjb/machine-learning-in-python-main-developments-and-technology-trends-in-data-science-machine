from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import pandas as pd
import os
from core.config import settings
from database.session import get_db
from models.dataset_metadata import DatasetMetadata
from core.preprocessing.pipeline import PreprocessingPipeline
from typing import Dict

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

@router.post("/{dataset_id}/process", status_code=status.HTTP_201_CREATED)
async def process_dataset(
    dataset_id: int,
    config: Dict,
    db: Session = Depends(get_db)
):
    # Fetch dataset metadata
    dataset = db.query(DatasetMetadata).filter(DatasetMetadata.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Load raw data
    raw_path = os.path.join(settings.data_dir, dataset.filename)
    if not os.path.exists(raw_path):
        raise HTTPException(status_code=404, detail="Raw data file not found")
    
    try:
        df = pd.read_csv(raw_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading data: {str(e)}")

    # Apply preprocessing
    try:
        pipeline = PreprocessingPipeline()
        processed_df = pipeline.transform(df, config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {str(e)}")

    # Save processed data
    processed_dir = os.path.join(settings.data_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_filename = f"processed_{dataset.filename}"
    processed_path = os.path.join(processed_dir, processed_filename)
    processed_df.to_csv(processed_path, index=False)

    # Create new metadata entry
    new_dataset = DatasetMetadata(
        filename=os.path.join("processed", processed_filename),
        file_type="csv",
        size=os.path.getsize(processed_path),
        columns=",".join(processed_df.columns),
        source_type="processed",
        connection_string=settings.database_url
    )
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return {
        "message": "Data preprocessing completed",
        "processed_dataset_id": new_dataset.id,
        "processed_columns": processed_df.columns.tolist()
    }
