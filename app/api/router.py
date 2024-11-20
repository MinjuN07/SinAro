from fastapi import APIRouter
from app.api.endpoints import sentiment, model, summary, letter

api_router = APIRouter()
api_router.include_router(model.router, prefix="/model", tags=["model"])
api_router.include_router(sentiment.router, prefix="/analyze", tags=["analysis"])
api_router.include_router(summary.router, prefix="/summarize", tags=["summary"])
api_router.include_router(letter.router, prefix="/generate", tags=["generate"])