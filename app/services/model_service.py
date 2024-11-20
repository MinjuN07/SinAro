from app.models.model import ModelInfoResponse
from app.core.constants import DEFAULT_MODEL_PARAMS
from app.services.base_service import BaseService

class ModelService(BaseService):
    async def get_model_info(self) -> ModelInfoResponse:
        """모델 정보를 조회합니다."""
        try:
            response = await self.client.get_model_info()
            models = response.get("models", [])
            
            model_info = next(
                (model for model in models
                if model.get("name") == self.model_name),
                None
            )
            
            return ModelInfoResponse(
                model_name=self.model_name,
                base_model="Llama-3.1-8B",
                parameters=DEFAULT_MODEL_PARAMS,
                status="loaded" if model_info else "unknown"
            )
        except Exception as e:
            self.logger.error(f"Error getting model info: {str(e)}")
            return ModelInfoResponse(
                model_name=self.model_name,
                base_model="Llama-3.1-8B",
                parameters=DEFAULT_MODEL_PARAMS,
                status=f"error: {str(e)}"
            )