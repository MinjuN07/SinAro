from fastapi import HTTPException

class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None
    ):
        self.error_code = error_code or f"ERR_{status_code}"
        super().__init__(status_code=status_code, detail=detail)

class ServiceError(APIError):
    def __init__(self, detail: str, error_code: str = None):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code=error_code or "SERVICE_ERROR"
        )

class ValidationError(APIError):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )

class NotFoundError(APIError):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found with identifier: {identifier}",
            error_code="NOT_FOUND"
        )

class EmptyTextError(ValidationError):
    def __init__(self):
        super().__init__(detail="Text cannot be empty")