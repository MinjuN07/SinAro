from fastapi import APIRouter, Depends, HTTPException, Response
from app.models.letter import LetterRequest
from app.services.letter_service import LetterService 
from app.dependencies import get_letter_service
import logging
import json



logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/letter")
async def generate_letter(
    request: LetterRequest,
    letter_service: LetterService = Depends(get_letter_service)
):
    """편지를 만드는 엔드포인트"""
    try:
        return await letter_service.generate_letter(request.id,request.day,request.text)
    except Exception as e:
        logger.error(f"예상치 못한 에러: {str(e)}")
        return Response(
            content=json.dumps({"error": str(e)}),
            media_type="application/json",
            status_code=500
        )