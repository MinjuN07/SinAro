from fastapi import HTTPException

class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class EmptyTextError(APIError):
    def __init__(self):
        super().__init__(status_code=400, detail="텍스트가 비어있습니다")