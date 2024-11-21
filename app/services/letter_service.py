from app.core.constants import SYSTEM_PROMPTS
from app.core.exceptions import APIError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
import os
import json
from typing import List, Dict

class LetterService(BaseService):
    def __init__(self):
        super().__init__(ModelType.LETTER)
        self.options = {
            "temperature": 0.8,
            "top_p": 0.95,
            "num_ctx": 4096,
            "frequency_penalty": 0.5
        }
        self.letter_data = self._load_letter_data()

    def _load_letter_data(self) -> Dict:
        """letter_data.json 파일에서 편지 데이터를 로드합니다."""
        try:
            file_path = os.path.join('app', 'data', 'letter_template.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading letter data: {str(e)}")
            return {}

    def _find_letter_template(self, id: str, day: str) -> str:
        """ID와 day에 해당하는 편지 템플릿을 찾습니다."""
        try:
            template = next(
                (letter['template'] for letter in self.letter_data 
                if str(letter['id']) == str(id) and str(letter['day']) == str(day)),
                None
            )
            if not template:
                raise APIError(
                    status_code=404,
                    detail=f"Template not found for ID {id} and day {day}"
                )
            return template
        except APIError:
            raise
        except Exception as e:
            self.logger.error(f"Error finding template: {str(e)}")
            raise APIError(
                status_code=500,
                detail=f"Error processing template: {str(e)}"
            )

    async def generate_letter(self, id: str, day: str, text: List[Dict[str, str]]):
        """편지를 생성합니다."""
        template = self._find_letter_template(id, day)
        
        text_data = [{"emotion": item.emotion, "keyword": item.keyword} for item in text]
        emotions_keywords_str = "\n".join([
            f"- 감정: {item['emotion']}, 키워드: {item['keyword']}" 
            for item in text_data
        ])

        prompt = f"""
            다음 감정과 키워드들 중 3가지를 자연스럽게 편지 템플릿에 추가해서 편지를 완성해줘:
            
            편지 템플릿 :
            {template}
            감정과 키워드 :
            {emotions_keywords_str}
            
            - template의 opening과 closing을 잘 지켜서 편지를 작성해줘
            - 키워드가 main_content에 잘 조화될 수 있게 편지를 작성해줘 
            - 한국어 문자열로만 이루어진 하나의 완성된 편지로 작성해줘
        """

        self.logger.debug(f"Generating letter for ID: {id}, Day: {day}")
        return await self._generate_response(prompt=prompt)