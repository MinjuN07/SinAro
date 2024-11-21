from app.core.model_config import ModelType
from app.services.base_service import BaseService

class SummaryService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SUMMARY)
        
    async def summarize_diary(self, text: str):
        """일기 텍스트를 요약합니다."""
        self.logger.debug(f"Summarizing diary with length: {len(text)}")
        prompt = f"""아래의 일기에서 감정과 관련된 정보를 중점으로 하여 최대 700자로 요약해줘.
        일기 : {text}
        """
        return await self._generate_response(prompt=prompt)