from fastapi import APIRouter, Depends
from app.models.health import HealthCheckResponse
from app.services.health_service import HealthService
from app.dependencies import get_health_service

router = APIRouter()

@router.get("/health",response_model=HealthCheckResponse)
async def health_check(
    health_service: HealthService = Depends(get_health_service)
):
    """시스템 헬스 체크를 수행하는 엔드포인트"""
    return await health_service.check_health()