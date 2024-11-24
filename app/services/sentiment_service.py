from app.core.exceptions import ValidationError, ServiceError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
import logging
import re

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)

    async def analyze_sentiment(self, text: str):
        self.logger.debug(f"Starting sentiment analysis. Text preview: {text[:100]}")
        
        if not text.strip():
            raise ValidationError("Text cannot be empty")
        
        response = await self._generate_response(prompt=text)
        
        self.logger.debug(f"Received model response: {response}")
        
        parsed_result = self._parse_response(response)
        
        self.logger.info(
            f"Sentiment analysis completed. "
            f"Emotion: {parsed_result['emotion']}, "
            f"Keyword: {parsed_result['keyword']}"
        )
        
        return parsed_result
        
    def _parse_response(self, response: str) -> dict:
        emotion_match = re.search(r"emotion\":\s*([^,]+)", response)
        keyword_match = re.search(r"keyword\":\s*([^\}]+)", response)
        
        if not emotion_match or not keyword_match:
            raise ServiceError(
                detail="Failed to parse model response",
                error_code="PARSE_ERROR"
            )
        
        return {
            "emotion": emotion_match.group(1).strip().strip('"\''),
            "keyword": keyword_match.group(1).strip().strip('"\'')
        }