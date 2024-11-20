import logging
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sentiment Analysis API"
    OLLAMA_API_BASE: str = "http://localhost:11434/api"
    OLLAMA_MODEL_NAME: str = "ko-llama-3.1-8b-uncensored"
    LOG_LEVEL: str = "DEBUG"

    model_config = ConfigDict(
        env_file=".env",
        extra='allow'
    )

def get_settings():
    return Settings()

settings = get_settings()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__all__ = ["settings"]