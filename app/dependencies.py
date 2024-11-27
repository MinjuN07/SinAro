from fastapi import Depends
from app.services.health_service import HealthService
from app.services.sentiment_service import SentimentAnalysisService
from app.services.letter_service import LetterService
import asyncio
from typing import Optional

_sentiment_service: Optional[SentimentAnalysisService] = None
_letter_service: Optional[LetterService] = None

def get_health_service():
    return HealthService()

async def get_sentiment_service():
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = SentimentAnalysisService()
        if hasattr(_sentiment_service, 'client'):
            await _sentiment_service.client.initialize()
    return _sentiment_service

async def get_letter_service():
    global _letter_service
    if _letter_service is None:
        _letter_service = LetterService()
        if hasattr(_letter_service, 'client'):
            await _letter_service.client.initialize()
    return _letter_service