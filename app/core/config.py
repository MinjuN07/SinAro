import logging
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sinavro"
    OLLAMA_API_BASE: str = "http://localhost:11434/api"
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)