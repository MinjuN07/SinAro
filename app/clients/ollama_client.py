import httpx
from app.core.config import settings
import logging
import json
from typing import Dict, Any, Optional
from fastapi import Response

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(300.0)
        
    async def generate(self, model: str, prompt: str, options: Optional[Dict[str, Any]] = None):
        try:
            request_data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            if options:
                request_data["options"] = options
                
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json=request_data
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