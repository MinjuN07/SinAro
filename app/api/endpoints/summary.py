from fastapi import APIRouter, Depends, HTTPException
from app.models.summary import SummaryRequest
from app.services.summary_service import SummaryService
from app.dependencies import get_summary_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/diary")
async def summarize_diary(
    request: SummaryRequest,
    summary_service: SummaryService = Depends(get_summary_service)
):
    """일기를 요약하는 엔드포인트"""
    try:
        logger.info("일기 요약 요청 받음")
        result = await summary_service.summarize_diary(request.text)
        logger.info("일기 요약 완료")
        return result
    except Exception as e:
        logger.error(f"일기 요약 중 에러: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
