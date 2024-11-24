from fastapi import APIRouter, Depends, Response
from app.models.sentiment import SentimentRequest
from app.services.sentiment_service import SentimentAnalysisService
from app.dependencies import get_sentiment_service
import logging
import json



logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/diary")
async def analyze_sentiment(
    request: SentimentRequest,
    sentiment_service: SentimentAnalysisService = Depends(get_sentiment_service)
):
    try:
        result = await sentiment_service.analyze_sentiment(request.text)
        return result
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        raise