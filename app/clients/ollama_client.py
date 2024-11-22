import httpx
from app.core.config import settings
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(300.0)
        
    async def generate(self, model: str, prompt: str, system: Optional[str] = None, options: Optional[Dict[str, Any]] = None):
        try:
            request_data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            if system:
                request_data["system"] = system
                
            if options:
                request_data["options"] = options
                
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json=request_data
                )
                return response.json()
                
        except Exception as e:
            logger.error(f"API 요청 실패: {str(e)}")
            raise