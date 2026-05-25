import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "AI Movie Recommendation Platform"
    VERSION: str = "1.0.0"

    MONGO_URI: str = Field(default="mongodb://localhost:27017/ai_movies")
    JWT_SECRET: str = Field(default="dev_secret_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    REDIS_URL: str = Field(default="redis://localhost:6379")
    CACHE_TTL_SECONDS: int = 3600

    TMDB_API_KEY: str = Field(default="")
    MODELS_DIR: str = Field(default="/models")

    RATE_LIMIT_PER_MINUTE: int = 60


@lru_cache()
def get_settings() -> Settings:
    env_models = os.getenv("MODELS_DIR")
    settings = Settings()
    if env_models:
        settings.MODELS_DIR = env_models
    elif not os.path.isabs(settings.MODELS_DIR):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        settings.MODELS_DIR = os.path.normpath(
            os.path.join(base, settings.MODELS_DIR)
        )
    return settings


settings = get_settings()
