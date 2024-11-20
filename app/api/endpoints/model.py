from fastapi import APIRouter, HTTPException
from app.models.model import ModelInfoResponse
from app.services.model_service import ModelService

router = APIRouter()
model_service = ModelService()

@router.get("/info", response_model=ModelInfoResponse)
async def get_model_info():
    """모델 정보를 조회하는 엔드포인트"""
    try:
        model_info = await model_service.get_model_info()
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))