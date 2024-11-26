from fastapi import APIRouter
from app.api.endpoints import sentiment, health, letter

api_router = APIRouter()
api_router.include_router(health.router, prefix="/system", tags=["system"])
api_router.include_router(sentiment.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(letter.router, prefix="/generate", tags=["generate"])