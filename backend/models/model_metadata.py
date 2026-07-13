from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from database.session import Base

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    job_id = Column(String, primary_key=True, index=True)
    algorithm = Column(String)
    parameters = Column(JSON)
    metrics = Column(JSON)
    status = Column(String)
    model_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())