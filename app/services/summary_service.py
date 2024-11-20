from app.core.constants import SYSTEM_PROMPTS
from app.services.base_service import BaseService

class SummaryService(BaseService):
    async def summarize_diary(self, text: str):
        """일기 텍스트를 요약합니다."""
        self.logger.debug(f"Summarizing diary with length: {len(text)}")
        return await self._generate_response(
            prompt=text,
            system_prompt=SYSTEM_PROMPTS["DIARY_SUMMARY"]
        )