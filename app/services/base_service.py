from app.clients.ollama_client import OllamaClient
from app.core.config import settings
from app.core.exceptions import APIError
import logging
from typing import Any, Dict

class BaseService:
    def __init__(self):
        self.client = OllamaClient()
        self.model_name = settings.OLLAMA_MODEL_NAME
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _generate_response(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        """공통 텍스트 생성 로직"""
        try:
            self.logger.debug(f"Generating response with prompt length: {len(prompt)}")
            response_data = await self.client.generate(
                model=self.model_name,
                system=system_prompt,
                prompt=prompt
            )
            self.logger.debug("Response generated successfully")
            return response_data
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}", exc_info=True)
            raise APIError(
                status_code=500,
                detail=f"Error generating response: {str(e)}"
            )