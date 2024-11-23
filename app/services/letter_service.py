from app.core.exceptions import APIError
from app.core.model_config import ModelType
from app.services.base_service import BaseService
import os
import json
from typing import List, Dict

class LetterService(BaseService):
    def __init__(self):
        super().__init__(ModelType.LETTER)
        self.letter_data = self._load_letter_data()

    def _load_letter_data(self) -> Dict:
        """letter_data.json 파일에서 편지 데이터를 로드합니다."""
        try:
            file_path = os.path.join('app', 'data', 'letter_data.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading letter data: {str(e)}")
            raise APIError(
                status_code=500,
                detail=f"Error loading letter data: {str(e)}"
            )

    def _find_letter_template(self, id: int, day: int) -> Dict:
        """ID와 day에 해당하는 편지 템플릿을 찾습니다."""
        template = next(
            (letter['template'] for letter in self.letter_data 
            if letter['id'] == id and letter['day'] == day),
            None
        )
        if not template:
            raise APIError(
                status_code=404,
                detail=f"Template not found for ID {id} and day {day}"
            )
        return template

    async def generate_letter(self, id: int, day: int, text: List[Dict[str, str]]):
        """편지를 생성합니다."""
        template = self._find_letter_template(id, day)
        
        prompt = f"""다음 편지를 기반으로 감정과 키워드를 자연스럽게 통합하여 편지를 완성해주세요:
원본 편지 : {template}
감정과 키워드 : {text}
요구사항:
1. 시작 부분과 끝맺음은 그대로 유지해줘
2. 주어진 감정과 키워드를 자연스럽게 편지 내용에 녹여줘
3. 편지의 전체적인 흐름을 자연스럽게 만들어줘
4. 편지의 말투를 고려해줘
5. 반드시 한국어로 작성해줘
6. 이모티콘은 사용하지마
7. 하나의 완성된 편지로 작성해줘"""

        self.logger.debug(f"Generating letter for ID: {id}, Day: {day}")
        return await self._generate_response(prompt=prompt)