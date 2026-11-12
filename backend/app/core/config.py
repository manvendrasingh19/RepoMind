
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "RepoMind"
    environment: str = "development"
    debug: bool = True

    frontend_url: str = "http://localhost:5173"
    api_v1_prefix: str = "/api/v1"

    mongodb_uri: str = "mongodb://localhost:27018"
    mongodb_database: str = "repomind"

    redis_url: str = "redis://localhost:6381/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "repository_code_embeddings"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
