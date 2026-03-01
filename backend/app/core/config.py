from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CVHT Smart Advisor API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg2://cvht:cvht123@localhost:5432/cvht_db"

    # JWT Authentication settings
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
