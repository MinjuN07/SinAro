from typing import Dict, Any
import httpx
from app.core.config import settings
import logging
import requests
from fastapi import FastAPI, Response
import json

from app.core.exceptions import APIError

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(1000.0)
        
    async def generate(self, model: str, system: str, prompt: str):
        try:
            res = requests.post(
                f"{self.base_url}/generate", 
                json={
                    "model": model,
                    "system": system,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            return Response(
                content=res.text,
                media_type="application/json"
            )
        
        except Exception as e:
            logger.error(f"API 요청 실패: {str(e)}")
            return Response(
                content=json.dumps({"error": str(e)}),
                media_type="application/json",
                status_code=500
            )
        
    async def get_model_info(self) -> Dict[str, Any]:
        """Ollama API에서 모델 정보를 가져옵니다."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.debug("모델 정보 요청")
                response = await client.get(f"{self.base_url}/tags")
                
                if response.status_code != 200:
                    error_detail = response.json() if response.content else "No error details"
                    logger.error(f"모델 정보 조회 실패 - Status: {response.status_code}, Details: {error_detail}")
                    raise APIError(
                        status_code=response.status_code,
                        detail=f"모델 정보 조회 실패: {error_detail}"
                    )
                
                return response.json()

        except httpx.RequestError as e:
            logger.error(f"모델 정보 요청 실패: {str(e)}")
            raise APIError(
                status_code=503,
                detail=f"Ollama 서비스 연결 실패: {str(e)}"
            )