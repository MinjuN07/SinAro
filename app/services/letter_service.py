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
            self.logger.info(
                f"Starting letter generation - ID: {id}, Day: {day}, "
                f"Emotions count: {len(text)}"
            )
            
            template = self._find_letter_template(id, day)
            
            emotions_keywords = "\n".join([
                f"- 감정: {item.emotion}, 키워드: {item.keyword}"
                for item in text
            ])
            
            prompt = self._create_prompt(template, emotions_keywords)
            response = await self._generate_response(prompt=prompt)
            
            self.logger.info(f"Letter generated successfully - ID: {id}, Day: {day}")
            return {"response": response}
            
        except Exception as e:
            self.logger.error(
                f"Letter generation failed - ID: {id}, Day: {day}, Error: {str(e)}"
            )
            raise
        
    def _load_letter_data(self) -> Dict:
        try:
            file_path = os.path.join('app', 'data', 'letter_data.json')
            self.logger.debug(f"Loading letter templates from: {file_path}")
            
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
        self.logger.debug(f"Searching for template - ID: {id}, Day: {day}")
        
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
        return f"""'다음 편지를 기반으로 감정과 키워드를 자연스럽게 통합하여 편지를 완성해주세요:
                    원본 편지: {template}

                    감정과 키워드 목록:
                    {emotions_keywords}

                    요구사항:
                    1. 시작 부분과 끝맺음은 그대로 유지해줘
                    2. 위의 감정과 키워드들을 자연스럽게 편지 내용에 녹여줘
                    3. 편지의 전체적인 흐름을 자연스럽게 만들어줘
                    4. 편지의 말투를 고려해줘
                    5. 반드시 한국어로 작성해줘
                    6. 이모티콘은 사용하지마
                    7. 하나의 완성된 편지로 작성해줘'"""