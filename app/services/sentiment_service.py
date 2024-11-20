from app.core.constants import SYSTEM_PROMPTS
from app.services.base_service import BaseService

class SentimentAnalysisService(BaseService):
    async def analyze_sentiment(self, text: str):
        """텍스트의 감정과 키워드를 분석합니다."""
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        return await self._generate_response(
            prompt=text,
            system_prompt=SYSTEM_PROMPTS["SENTIMENT_ANALYSIS"]
        )