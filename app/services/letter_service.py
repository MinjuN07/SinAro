from app.core.exceptions import NotFoundError, ServiceError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
from app.models.letter import EmotionKeyword
import os
import json
from typing import List, Dict

class LetterService(BaseService):
    def __init__(self):
        super().__init__(ModelType.LETTER)
        self.letter_data = self._load_letter_data()
        self.logger.info("Letter service initialized")

    async def generate_letter(self, id: int, day: int, text: List[EmotionKeyword]):
        try:
            self.logger.info(f"Emotions count: {len(text)}")
            
            template = self._find_letter_template(id, day)
            
            emotions_keywords = "\n".join([
                f"- 감정: {item.emotion}, 키워드: {item.keyword}"
                for item in text
            ])
            
            prompt = self._create_prompt(template, emotions_keywords)
            response = await self._generate_response(prompt=prompt)
            
            self.logger.info(f"Letter generated successfully. response length: {len(response)}")
            return {"response": response}
            
        except Exception as e:
            self.logger.error(
                f"Letter generation failed - ID: {id}, Day: {day}, Error: {str(e)}"
            )
            raise
        
    def _load_letter_data(self) -> Dict:
        try:
            file_path = os.path.join('app', 'data', 'letter_data.json')
            self.logger.info(f"Loading letter templates from: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.info(f"Letter templates loaded successfully. Count: {len(data)}")
                return data
                
        except Exception as e:
            self.logger.error(f"Failed to load letter templates: {str(e)}")
            raise ServiceError(
                detail="Failed to load letter templates",
                error_code="TEMPLATE_LOAD_ERROR"
            )

    def _find_letter_template(self, id: int, day: int) -> str:
        self.logger.info(f"Searching for template - ID: {id}, Day: {day}")
        
        template = next(
            (letter['text'] for letter in self.letter_data 
            if letter['id'] == id and letter['day'] == day),
            None
        )
        
        if not template:
            raise NotFoundError(
                resource="Letter template",
                identifier=f"id={id}, day={day}"
            )
            
        return template

    def _create_prompt(self, template: str, emotions_keywords: str) -> str:
        return f"""###원본 편지### 
                    {template}
                    
                    ###감정과 키워드 목록###
                    {emotions_keywords}"""