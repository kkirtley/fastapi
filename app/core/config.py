""" Configuration settings for the FastAPI application."""
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.
    This class uses Pydantic to manage application settings,
    including environment variables and default values.
    """
    PROJECT_NAME: str = "FastAPI Scaffold"
    VERSION: str = "1.0.0"
    ENV: str = "production"  # Default to production
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DB_MAX_RETRIES: int = 5
    DB_RETRY_BASE_DELAY: float = 1.0
    DB_RETRY_MAX_DELAY: float = 10.0
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000"]
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str

    # Google OAuth settings (optional in non-production)
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    SECRET_KEY: str | None = None  # For JWT and session middleware
    FRONTEND_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'production')}",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """Check if the current environment is production."""
        return self.ENV == "production"

settings = Settings()
