from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME : str = "Articles Hub API"
    ENVIROMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    SECRET_KEY: str = Field(..., min_length=16)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, gt=0)
