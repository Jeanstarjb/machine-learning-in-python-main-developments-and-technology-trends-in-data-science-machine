from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.dataset_metadata import DatasetMetadata
from core.config import settings
from core.cloud_storage import S3Client
import pandas as pd
import io
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
    local_file_path = f"{settings.data_dir}/{filename}"
    with open(local_file_path, "wb") as f:
        f.write(contents)

    # Upload file to S3
    s3_client = S3Client()
    s3_path = s3_client.upload_file(local_file_path, f"datasets/{filename}")

    # Save metadata to database
    dataset_metadata = DatasetMetadata(
        filename=filename,
        file_type="csv",
        size=len(contents),
        columns=",".join(df.columns),
        source_type="s3",
        connection_string=s3_path
    )
    db.add(dataset_metadata)
    db.commit()
    db.refresh(dataset_metadata)

    return {"message": "File uploaded successfully", "s3_path": s3_path, "dataset_id": dataset_metadata.id}
