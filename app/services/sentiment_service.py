from app.core.exceptions import ValidationError, ServiceError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
import re

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)

    async def analyze_sentiment(self, text: str):
        self.logger.debug("Starting sentiment analysis", text_preview=text[:100])
        
        if not text.strip():
            raise ValidationError("Text cannot be empty")
        
        response = await self._generate_response(prompt=text)
        
        self.logger.debug("Received model response", response=response)
        
        analyze_result = self._analyze_response(response)
        
        self.logger.info(
            "Sentiment analysis completed",
            emotion=analyze_result['emotion'],
            keyword=analyze_result['keyword']
        )
        
        return analyze_result
        
    def _analyze_response(self, response: str) -> dict:
        emotion_match = re.search(r"emotion:\s*([^,]+)", response)
        keyword_match = re.search(r"keyword:\s*([^\}]+)", response)
        
        if not emotion_match or not keyword_match:
            raise ServiceError(
                detail="Failed to analyze model response",
                error_code="ANALYZE_ERROR"
            )
        
        return {
            "emotion": emotion_match.group(1).strip().strip('"\''),
            "keyword": keyword_match.group(1).strip().strip('"\'')
        }