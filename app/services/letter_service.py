from app.core.exceptions import APIError
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
        self.logger.info("LetterService initialized")

    def _load_letter_data(self) -> Dict:
        """letter_data.json 파일에서 편지 데이터를 로드합니다."""
        try:
            file_path = os.path.join('app', 'data', 'letter_data.json')
            self.logger.debug(f"Loading letter data from: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.info(f"Letter data loaded successfully. count: {len(data)}")
                return data
                
        except Exception as e:
            self.logger.error(f"Failed to load letter data: {str(e)}")
            raise APIError(
                status_code=500,
                detail="Failed to load letter"
            )

    def _find_letter_leeter(self, id: int, day: int) -> str:
        """ID와 day에 해당하는 편지를 찾습니다."""
        self.logger.debug(f"Searching for letter - ID: {id}, Day: {day}")
        
        template = next(
            (letter['text'] for letter in self.letter_data 
            if letter['id'] == id and letter['day'] == day),
            None
        )
        
        if not template:
            self.logger.error(f"Template not found - ID: {id}, Day: {day}")
            raise APIError(
                status_code=404,
                detail=f"Template not found for ID {id} and day {day}"
            )
            
        self.logger.debug(f"Template found successfully - ID: {id}, Day: {day}")
        return template

    async def generate_letter(self, id: int, day: int, text: List[EmotionKeyword]):
        """편지를 생성합니다."""
        try:
            self.logger.info(
                f"Starting letter generation - "
                f"ID: {id}, Day: {day}, "
                f"Number of emotions/keywords: {len(text)}"
            )
            
            template = self._find_letter_letter(id, day)
            
            emotions_keywords = "\n".join([
                f"- 감정: {item.emotion}, 키워드: {item.keyword}"
                for item in text
            ])
            
            prompt = f"""다음 편지를 기반으로 감정과 키워드를 자연스럽게 통합하여 편지를 완성해주세요:
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
7. 하나의 완성된 편지로 작성해줘"""

            self.logger.debug(f"Prompt created for letter generation - ID: {id}, Day: {day}")
            
            response = await self._generate_response(prompt=prompt)
            
            self.logger.info(f"Letter generated successfully - ID: {id}, Day: {day}")
            return {"response": response}
            
        except APIError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in letter generation: {str(e)}", exc_info=True)
            raise APIError(
                status_code=500,
                detail="Failed to generate letter"
            )