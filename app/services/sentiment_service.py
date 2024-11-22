from app.core.model_config import ModelType
from app.services.base_service import BaseService
import json

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
            "stop": ["\n\n\n","\n\n","\n"]
        }

    async def analyze_sentiment(self, text: str):
        self.logger.debug(f"Analyzing text: {text[:100]}...")
        response = await self._generate_response(
            prompt=text,
            options=self.options
        )
        
        try:
            ollama_response = json.loads(response)
            sentiment_response = ollama_response.get('response', '{}')
            sentiment_response = sentiment_response.replace("emotion:", '"emotion":').replace("keyword:", '"keyword":')
            parsed_response = json.loads(sentiment_response)
            
            return {
                "emotion": parsed_response.get("emotion", ""),
                "keyword": parsed_response.get("keyword", "")
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse response: {e}")
            return {
                "emotion": "",
                "keyword": "" 
            }