from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.dataset_metadata import DatasetMetadata
from core.config import settings
import pandas as pd
import io
import os
from werkzeug.utils import secure_filename

router = APIRouter(prefix="/data", tags=["Data Ingestion"])

@router.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV file: {str(e)}"
        )
    
    filename = secure_filename(file.filename)
    upload_dir = os.path.join(settings.data_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    db_record = DatasetMetadata(
        filename=filename,
        file_type="csv",
        size=len(contents),
        columns=",".join(df.columns.tolist()),
        source_type="upload"
    )
    db.add(db_record)
    db.commit()
    
    return {"filename": filename, "columns": df.columns.tolist(), "message": "File uploaded successfully"}

@router.post("/upload/json")
async def upload_json(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_json(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON file: {str(e)}"
        )
    
    filename = secure_filename(file.filename)
    upload_dir = os.path.join(settings.data_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    db_record = DatasetMetadata(
        filename=filename,
        file_type="json",
        size=len(contents),
        columns=",".join(df.columns.tolist()),
        source_type="upload"
    )
    db.add(db_record)
    db.commit()
    
    return {"filename": filename, "columns": df.columns.tolist(), "message": "File uploaded successfully"}

@router.post("/connect/database")
async def connect_database(connection_str: str, db: str = Depends(get_db)):
    from sqlalchemy import create_engine, inspect
    from sqlalchemy.exc import SQLAlchemyError
    
    try:
        engine = create_engine(connection_str)
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            return {"status": "success", "tables": tables}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database connection failed: {str(e)}"
        )