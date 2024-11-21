from app.core.model_config import ModelType
from app.services.base_service import BaseService

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)
        
    async def analyze_sentiment(self, text: str):
        """텍스트의 감정과 키워드를 분석합니다."""
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        return await self._generate_response(prompt=text)