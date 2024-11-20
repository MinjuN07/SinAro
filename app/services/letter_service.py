from app.core.constants import SYSTEM_PROMPTS
from app.core.exceptions import APIError
from app.services.base_service import BaseService
import os
import json
from typing import List, Dict

class LetterService(BaseService):
    def __init__(self):
        super().__init__()
        self.letter_data = self._load_letter_data()

    def _load_letter_data(self) -> Dict:
        """letter_data.json 파일에서 편지 데이터를 로드합니다."""
        try:
            file_path = os.path.join('app', 'data', 'letter_data.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading letter data: {str(e)}")
            return {}

    def _find_letter_template(self, id: str, day: str) -> str:
        """ID와 day에 해당하는 편지 템플릿을 찾습니다."""
        try:
            template = next(
                (letter['text'] for letter in self.letter_data 
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
        
        emotions_keywords_str = "\n".join([
            f"- 감정: {item['emotion']}, 키워드: {item['keyword']}" 
            for item in text
        ])

        prompt = f"""아래의 기존 편지를 기반으로 하되, 주어진 감정과 키워드들 중 3가지를 자연스럽게 통합하여 완성된 하나의 편지로 만들어줘.
                    기존 편지:
                    {template}
                    감정과 그 감정에 대한 키워드:
                    {emotions_keywords_str}
        """

        self.logger.debug(f"Generating letter for ID: {id}, Day: {day}")
        return await self._generate_response(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPTS["LETTER_GENERATE"]
        )