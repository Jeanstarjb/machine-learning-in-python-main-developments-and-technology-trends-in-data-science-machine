from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.dataset_metadata import DatasetMetadata
from core.config import settings
from core.cloud_storage import S3Client
import pandas as pd
import io
from werkzeug.utils import secure_filename
from core.security import get_current_active_user

router = APIRouter(prefix="/data", tags=["Data Ingestion"], dependencies=[Depends(get_current_active_user)])

@router.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Save to cloud storage
        s3_client = S3Client()
        filename = secure_filename(file.filename)
        local_path = f"{settings.data_dir}/{filename}"
        with open(local_path, "wb") as f:
            f.write(contents)
        s3_path = f"uploads/{filename}"
        s3_client.upload_file(local_path, s3_path)
        
        # Store metadata
        metadata = DatasetMetadata(
            filename=filename,
            file_type="csv",
            size=len(contents),
            columns=",".join(df.columns),
            source_type="s3",
            connection_string=s3_path
        )
        db.add(metadata)
        db.commit()
        return {"message": "File uploaded successfully", "s3_path": s3_path}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))