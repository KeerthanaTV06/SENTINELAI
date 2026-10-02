"""Configuration module using Pydantic settings."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file.

    Attributes
    ----------
    FASTAPI_HOST: str
        Host for FastAPI.
    FASTAPI_PORT: int
        Port for FastAPI.
    KAFKA_BROKER: str
        Kafka broker address.
    ELASTIC_HOST: str
        Elasticsearch host.
    ELASTIC_PORT: int
        Elasticsearch port.
    """

    FASTAPI_HOST: str = Field(default="0.0.0.0", validation_alias="FASTAPI_HOST")
    FASTAPI_PORT: int = Field(default=8000, validation_alias="FASTAPI_PORT")

    KAFKA_BROKER: str = Field(default="localhost:9092", validation_alias="KAFKA_BROKER")
    KAFKA_TOPIC_NSLKDD: str = Field(default="nslkdd", validation_alias="KAFKA_TOPIC_NSLKDD")
    KAFKA_TOPIC_CICIDS: str = Field(default="cicids", validation_alias="KAFKA_TOPIC_CICIDS")

    ELASTIC_HOST: str = Field(default="localhost", validation_alias="ELASTIC_HOST")
    ELASTIC_PORT: int = Field(default=9200, validation_alias="ELASTIC_PORT")
    ELASTIC_HTTP_SCHEME: str = Field(default="http", validation_alias="ELASTIC_HTTP_SCHEME")

    APP_ENV: str = Field(default="development", validation_alias="APP_ENV")
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    MLFLOW_TRACKING_URI: str = Field(default="http://mlflow:5000", validation_alias="MLFLOW_TRACKING_URI")
    DVC_REMOTE: str = Field(default="local", validation_alias="DVC_REMOTE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


def get_settings() -> Settings:
    """Return a Settings instance.

    Returns
    -------
    Settings
        Application settings loaded from environment.
    """
    return Settings()
