from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ML Platform"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./mlplatform.db"
    data_dir: str = "./data"

    class Config:
        env_file = ".env"

settings = Settings()