"""Application configuration settings."""

from typing import Annotated, List, Union

from pydantic import BeforeValidator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_string_list(v: Union[str, List[str]]) -> List[str]:
    """Parse a comma-separated string into a list."""
    if isinstance(v, str):
        return [item.strip() for item in v.split(",")]
    return v


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        json_schema_extra={"ignore": True},
    )

    APP_NAME: str = "MemoryVault"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    API_V1_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    DATABASE_URL: str
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    REDIS_URL: str = "redis://localhost:6379/0"

    CORS_ORIGINS: str = "http://localhost:3000"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins as list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> List[str]:
        """Parse CORS methods as list."""
        return [method.strip() for method in self.CORS_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> List[str]:
        """Parse CORS headers as list."""
        return [header.strip() for header in self.CORS_HEADERS.split(",")]

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.7
    WHISPER_MODEL: str = "whisper-1"

    ELEVENLABS_API_KEY: str = ""

    PINATA_API_KEY: str = ""
    PINATA_SECRET_KEY: str = ""
    PINATA_JWT: str = ""

    EMAIL_ENABLED: bool = False
    EMAIL_FROM: str = "noreply@memvault.com"
    EMAIL_FROM_NAME: str = "MemoryVault"
    SENDGRID_API_KEY: str = ""

    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    MAX_UPLOAD_SIZE: int = 524288000
    TEMP_STORAGE_PATH: str = "/tmp/memvault"
    ALLOWED_AUDIO_FORMATS: str = "mp3,wav,m4a,ogg,flac"

    @property
    def allowed_audio_formats_list(self) -> List[str]:
        """Parse allowed audio formats as list."""
        return [fmt.strip() for fmt in self.ALLOWED_AUDIO_FORMATS.split(",")]

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    SENTRY_DSN: str = ""
    SENTRY_ENVIRONMENT: str = "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"


settings = Settings()  # type: ignore[call-arg]
