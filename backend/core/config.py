from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ML Platform"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./mlplatform.db"
    data_dir: str = "./data"
    model_dir: str = "./models"  # Added model directory

    class Config:
        env_file = ".env"

settings = Settings()