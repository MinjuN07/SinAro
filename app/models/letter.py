from pydantic import BaseModel, Field
from typing import List

class EmotionKeyword(BaseModel):
    emotion: str = Field(..., description="감정")
    keyword: str = Field(..., description="키워드")

class LetterRequest(BaseModel):
    id: int = Field(..., description="편지 주인의 ID")
    day: int = Field(..., description="편지의 순서")
    text: List[EmotionKeyword] = Field(..., description="감정과 키워드 데이터")