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
            "num_ctx": 8096,
            "num_predict": 4048,
            "temperature": 0.5,
            "top_p": 0.7,
            "top_k": 20,
            "frequency_penalty": 0.5,
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

    def _find_letter_template(self, id: str, day: str) -> Dict:
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
        
        opening = template['opening']
        main_themes = [
            f"- {content['theme']} (감정: {content['emotion']}, 키워드: {content['keyword']})"
            for content in template['main_content']
        ]
        closing = template['closing']

        new_emotions_keywords = [
            f"- 감정: {item.emotion}, 키워드: {item.keyword}" 
            for item in text
        ]

        prompt = f"""다음 편지 템플릿을 기반으로 새로운 감정과 키워드를 자연스럽게 통합하여 편지를 완성해주세요:

시작 부분:
{opening}

원래 편지의 주요 테마:
{chr(10).join(main_themes)}

새롭게 통합할 감정과 키워드:
{chr(10).join(new_emotions_keywords)}

끝맺음:
{closing}

요구사항:
1. 시작 부분과 끝맺음은 그대로 유지해주세요
2. 주어진 새로운 감정과 키워드를 자연스럽게 편지 내용에 녹여주세요
3. 편지의 전체적인 흐름을 자연스럽게 만들어주세요
4. 반드시 한국어로 작성해주세요
5. 이모티콘은 사용하지 말아주세요
6. 하나의 완성된 편지로 작성해주세요"""

        self.logger.debug(f"Generating letter for ID: {id}, Day: {day}")
        return await self._generate_response(
            prompt=prompt,
            options=self.options
        )