from app.models.health import HealthCheckResponse
from app.core.model_config import ModelType
import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class HealthService:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(10.0) 
        
    async def check_health(self) -> HealthCheckResponse:
        """시스템 전반의 헬스 체크를 수행합니다."""
        services_status = {}
        overall_status = "healthy"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/tags")
                if response.status_code == 200:
                    services_status["ollama_api"] = "healthy"
                    
                    models = {model.get("name") for model in response.json().get("models", [])}
                    for model_type in ModelType:
                        if model_type.value in models:
                            services_status[f"model_{model_type.name.lower()}"] = "loaded"
                        else:
                            services_status[f"model_{model_type.name.lower()}"] = "not_loaded"
                            overall_status = "degraded"
                else:
                    services_status["ollama_api"] = "unhealthy"
                    overall_status = "unhealthy"
                    
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            services_status["ollama_api"] = f"error: {str(e)}"
            overall_status = "unhealthy"

        return HealthCheckResponse(
            status=overall_status,
            services=services_status
        )
