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
                        "num_ctx": 8096,
                        "temperature": 0.2,
                        "top_p": 0.3,
                        "top_k": 20,
                        "num_predict": 2100,
                        "repeat_penalty": 1.5,
                        "presence_penalty": 0.5,
                        "frequency_penalty": 0.3,
                        "mirostat": 1,
                        "mirostat_tau": 0.5,
                        "stop": ["\n\n\n"]
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