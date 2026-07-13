from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.session import Base

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_type = Column(String)
    size = Column(Integer)
    columns = Column(String)
    source_type = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    connection_string = Column(String, nullable=True)