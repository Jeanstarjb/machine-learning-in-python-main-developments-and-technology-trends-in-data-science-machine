from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ML Platform"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./mlplatform.db"
    data_dir: str = "./data"
    model_dir: str = "./models"
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    s3_bucket_name: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()