from pydantic import BaseModel
from typing import Dict, Any

class ModelInfoResponse(BaseModel):
    model_name: str
    base_model: str
    parameters: Dict[str, Any]
    status: str