from pydantic import BaseModel, Field

class SummaryRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="요약할 일기 텍스트",
        example="오늘은 친구와 카페에서 만나 오랜만에 이야기를 나누었다..."
    )

class SummaryResponse(BaseModel):
    summary: str = Field(
        ...,
        max_length=700,
        description="요약된 일기"
    )