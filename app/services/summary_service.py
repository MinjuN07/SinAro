from app.core.model_config import ModelType
from app.services.base_service import BaseService

class SummaryService(BaseService):
    def __init__(self):
        super().__init__(ModelType.SUMMARY)
        
    async def summarize_diary(self, text: str):
        """일기 텍스트를 요약합니다."""
        self.logger.debug(f"Summarizing diary with length: {len(text)}")
        prompt = f"""아래 일기의 문체와 감정을 그대로 유지하면서 핵심 내용만 700자 이내로 요약해줘. 
        원문의 표현을 최대한 살려서 자연스럽게 요약해줘.
        
        일기 : {text}
        """
        return await self._generate_response(prompt=prompt)