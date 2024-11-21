import httpx
from app.core.config import settings
import logging
import json
from fastapi import Response

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(300.0)
        
    async def generate(self, model: str, prompt: str):
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 20000,
                        "temperature": 0.3,
                        "top_p": 0.4,
                        "top_k": 40,
                        "num_predict": 2048,
                        "repeat_penalty": 1.2,
                        "presence_penalty": 0.3,
                        "frequency_penalty": 0.3
                    }
                }
                )
                
                return Response(
                    content=response.text,
                    media_type="application/json"
                )
        except Exception as e:
            logger.error(f"API 요청 실패: {str(e)}")
            return Response(
                content=json.dumps({"error": str(e)}),
                media_type="application/json",
                status_code=500
            )