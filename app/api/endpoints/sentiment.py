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
    """일기를 분석하는 엔드포인트"""
    try:
        return await sentiment_service.analyze_sentiment(request.text)
    except Exception as e:
        logger.error(f"예상치 못한 에러: {str(e)}")
        return Response(
            content=json.dumps({"error": str(e)}),
            media_type="application/json",
            status_code=500
        )