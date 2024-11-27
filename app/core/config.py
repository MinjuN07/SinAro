import logging
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sinabro"
    OLLAMA_API_BASE: str = "http://localhost:11434/api"
    LOG_LEVEL: str = "INFO"

    OLLAMA_MAX_CONCURRENT_REQUESTS: int = 2 
    OLLAMA_MAX_QUEUE_SIZE: int = 50         
    OLLAMA_CONNECT_TIMEOUT: float = 10.0      
    OLLAMA_READ_TIMEOUT: float = 240.0   
    OLLAMA_WRITE_TIMEOUT: float = 10.0            
    OLLAMA_POOL_TIMEOUT: float = 10.0

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