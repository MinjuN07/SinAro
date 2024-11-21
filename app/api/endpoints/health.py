from fastapi import APIRouter
from app.models.health import HealthCheckResponse
from app.services.health_service import HealthService

router = APIRouter()
health_service = HealthService()

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """시스템 헬스 체크를 수행하는 엔드포인트"""
    return await health_service.check_health()