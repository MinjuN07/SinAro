from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(..., 
                    min_length=1, 
                    max_length=10000, 
                    description="분석할 텍스트",
                    example="오늘은 정말 행복한 하루였어. 친구들과 맛있는 점심을 먹었지.")

class SentimentResponse(BaseModel):
    emotion: str
    keyword: str