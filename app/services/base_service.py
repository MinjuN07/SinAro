from app.clients.ollama_client import OllamaClient
from app.core.config import settings
from app.core.model_config import ModelType, MODEL_SYSTEM, MODEL_OPTIONS
from app.core.exceptions import APIError
import logging
from typing import Any, Dict, Optional

class BaseService:
    def __init__(self, model_type: ModelType):
        self.client = OllamaClient()
        self.model_name = model_type.value
        self.logger = logging.getLogger(self.__class__.__name__)
        self.system = MODEL_SYSTEM.get(model_type, "")
        self.options = MODEL_OPTIONS.get(model_type, {})

    async def _generate_response(self, prompt: str) -> str:
        """공통 텍스트 생성 로직"""
        try:
            self.logger.debug(f"Generating response with prompt length: {len(prompt)}")
            response_data = await self.client.generate(
                model=self.model_name,
                prompt=prompt,
                system=self.system,
                options=self.options
            )
            
            if 'error' in response_data:
                raise APIError(
                    status_code=500,
                    detail=response_data['error']
                )
                
            if 'response' not in response_data:
                raise APIError(
                    status_code=500,
                    detail="Invalid response format from model"
                )
                
            return response_data['response']
            
        except APIError:
            raise
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise APIError(
                status_code=500,
                detail=f"Error generating response: {str(e)}"
            )