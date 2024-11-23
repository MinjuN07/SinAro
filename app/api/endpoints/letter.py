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
    """편지를 만드는 엔드포인트"""
    try:
        result = await letter_service.generate_letter(
            id=request.id,
            day=request.day,
            text=request.text
        )

        return result
        
    except APIError as e:
        logger.error(
            f"API error occurred while generating letter - "
            f"ID: {request.id}, Day: {request.day}, "
            f"Error: {str(e)}"
        )
        return Response(
            content=json.dumps({"error": e.detail}),
            media_type="application/json",
            status_code=e.status_code
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while generating letter - "
            f"ID: {request.id}, Day: {request.day}",
            exc_info=True
        )
        return Response(
            content=json.dumps({"error": "Internal server error"}),
            media_type="application/json",
            status_code=500
        )