import httpx
import asyncio
from app.core.config import settings
from app.core.exceptions import ServiceError
import logging
from typing import Dict, Any, Optional
from asyncio import Queue

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_API_BASE
        self.timeout = httpx.Timeout(
            connect=settings.OLLAMA_CONNECT_TIMEOUT,
            read=settings.OLLAMA_READ_TIMEOUT,
            write=settings.OLLAMA_WRITE_TIMEOUT,
            pool=settings.OLLAMA_POOL_TIMEOUT
        )
        self.max_concurrent_requests = settings.OLLAMA_MAX_CONCURRENT_REQUESTS
        self.max_queue_size = settings.OLLAMA_MAX_QUEUE_SIZE
        
        self._queue = Queue(maxsize=self.max_queue_size)
        self._workers = []
        self._initialized = False
        
        logger.info(
            f"Created OllamaClient with {self.max_concurrent_requests} workers "
            f"and queue size {self.max_queue_size}"
        )

    async def initialize(self):
        if not self._initialized:
            self._workers = [
                asyncio.create_task(self._worker(i))
                for i in range(self.max_concurrent_requests)
            ]
            self._initialized = True
            logger.info("OllamaClient workers initialized")

    async def generate(self, model: str, prompt: str, system: Optional[str] = None, options: Optional[Dict[str, Any]] = None):
        if not self._initialized:
            await self.initialize()
            
        future = asyncio.Future()
        await self._queue.put((future, model, prompt, system, options))
        logger.info(f"Request queued. Current queue size: {self._queue.qsize()}")
        return await future

    async def _worker(self, worker_id: int):
        logger.info(f"Starting worker {worker_id}")
        while True:
            try:
                future, model, prompt, system, options = await self._queue.get()
                try:
                    result = await self._process_request(model, prompt, system, options)
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
                finally:
                    self._queue.task_done()
                    
            except Exception as e:
                logger.error(f"Worker {worker_id} encountered error: {str(e)}")
                await asyncio.sleep(1)
        
    async def _process_request(self, model: str, prompt: str, system: Optional[str] = None, options: Optional[Dict[str, Any]] = None):
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
                
                if response.status_code != 200:
                    error_msg = f"Ollama API returned status {response.status_code}"
                    logger.error(f"{error_msg}: {response.text}")
                    raise ServiceError(detail=error_msg, error_code="OLLAMA_API_ERROR")
                
                return response.json()
                
        except httpx.TimeoutException as e:
            error_msg = f"Request to Ollama API timed out after {self.timeout.read} seconds"
            logger.error(error_msg)
            raise ServiceError(detail=error_msg, error_code="OLLAMA_TIMEOUT")
            
        except httpx.RequestError as e:
            error_msg = f"Failed to connect to Ollama API: {str(e)}"
            logger.error(error_msg)
            raise ServiceError(detail=error_msg, error_code="OLLAMA_CONNECTION_ERROR")
            
        except Exception as e:
            error_msg = f"Unexpected error in Ollama API request: {str(e)}"
            logger.error(error_msg)
            raise ServiceError(detail=error_msg, error_code="OLLAMA_UNEXPECTED_ERROR")