# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Scaffold"
    VERSION: str = "1.0.0"
    ENV: str
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DB_MAX_RETRIES: int = 5
    DB_RETRY_BASE_DELAY: float = 1.0
    DB_RETRY_MAX_DELAY: float = 10.0
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000"]
    LOG_LEVEL: str = "INFO"

    # Add database fields
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"  # Default port
    POSTGRES_HOST: str = "localhost"  # Default host
    DATABASE_URL: str
    COMPOSE_BAKE: bool


    # @property
    # def database_url(self) -> str:
    #     """Construct the DATABASE_URL dynamically."""
    #     return (
    #         f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
    #         f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    #     )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
