from fastapi import APIRouter, Depends, Response
from app.models.letter import LetterRequest
from app.services.letter_service import LetterService 
from app.dependencies import get_letter_service
from app.core.exceptions import APIError
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/letter")
async def generate_letter(
    request: LetterRequest,
    letter_service: LetterService = Depends(get_letter_service)
):
    try:
        result = await letter_service.generate_letter(
            id=request.id,
            day=request.day,
            text=request.text
        )
        return result
    except Exception as e:
        logger.error(f"Letter generation failed: {str(e)}")
        raise