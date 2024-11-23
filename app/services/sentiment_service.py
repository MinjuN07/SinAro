from app.core.model_config import ModelType, MODEL_OPTIONS
from app.services.base_service import BaseService
import re

class SentimentAnalysisService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SENTIMENT)
        self.options = MODEL_OPTIONS[ModelType.SENTIMENT]

    async def analyze_sentiment(self, text: str):
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        response = await self._generate_response(
            prompt=text,
            options=self.options
        )
        
        try:
            cleaned_response = response.replace("'", "").replace('"', "")
            
            emotion_match = re.search(r"emotion:\s*([^,]+)", cleaned_response)
            keyword_match = re.search(r"keyword:\s*([^\}]+)", cleaned_response)
            
            emotion = emotion_match.group(1).strip() if emotion_match else ""
            keyword = keyword_match.group(1).strip() if keyword_match else ""
            
            return {
                "response": {
                    "emotion": emotion,
                    "keyword": keyword
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse response: {e}")
            return {
                "response": {
                    "emotion": "",
                    "keyword": ""
                }
            }