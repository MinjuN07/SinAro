from app.core.model_config import ModelType
from app.services.base_service import BaseService

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)
        self.options = {
            "num_ctx": 8096,
            "temperature": 0.2,
            "top_p": 0.3,
            "top_k": 20,
            "num_predict": 1024,
            "repeat_penalty": 1.5,
            "presence_penalty": 0.5,
            "frequency_penalty": 0.3,
            "mirostat": 1,
            "mirostat_tau": 0.5,
            "stop": ["\n\n\n"]
        }

    async def analyze_sentiment(self, text: str):
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        return await self._generate_response(
            prompt=text,
            options=self.options
        )