from app.core.exceptions import APIError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
import re

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)

    async def analyze_sentiment(self, text: str):
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        response = await self._generate_response(prompt=text)
        
        self.logger.debug(f"Raw response from model: {response}")
        
        emotion_match = re.search(r"emotion:\s*([^,]+)", response)
        keyword_match = re.search(r"keyword:\s*([^\}]+)", response)
        
        self.logger.debug(f"Emotion match: {emotion_match}, Keyword match: {keyword_match}")
        
        if not emotion_match or not keyword_match:
            raise APIError(
                status_code=422,
                detail="Failed to parse emotion or keyword from response. "
                    f"Response format was unexpected: {response[:200]}"
            )
        
        emotion = emotion_match.group(1).strip()
        keyword = keyword_match.group(1).strip()
        
        self.logger.debug(f"Parsed result - Emotion: {emotion}, Keyword: {keyword}")
        
        return {
            "emotion": emotion,
            "keyword": keyword
        }