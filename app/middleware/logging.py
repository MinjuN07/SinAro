from fastapi import Request
import time
import logging

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"Path: {request.url.path} Process Time: {process_time:.2f}s")
    return response