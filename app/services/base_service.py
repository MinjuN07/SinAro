from app.core.exceptions import ServiceError, APIError
from app.clients.ollama_client import OllamaClient
from app.core.model_config import ModelType, MODEL_NAME, MODEL_SYSTEM, MODEL_OPTIONS
import logging

class BaseService:
    def __init__(self, model_type: ModelType):
        self.client = OllamaClient()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.model_name = MODEL_NAME.get(model_type, "")
        self.system = MODEL_SYSTEM.get(model_type, "")
        self.options = MODEL_OPTIONS.get(model_type, {})

    async def _generate_response(self, prompt: str) -> str:
        try:
            response_data = await self.client.generate(
                model=self.model_name,
                prompt=prompt,
                system=self.system,
                options=self.options
            )
            
            if 'error' in response_data:
                raise ServiceError(
                    detail=response_data['error'],
                    error_code="MODEL_ERROR"
                )
                
            if 'response' not in response_data:
                raise ServiceError(
                    detail="Invalid response format from model",
                    error_code="INVALID_RESPONSE"
                )
                
            return response_data['response']
            
        except APIError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to generate response: {str(e)}")
            raise ServiceError(
                detail="Failed to generate response",
                error_code="GENERATION_ERROR"
            )