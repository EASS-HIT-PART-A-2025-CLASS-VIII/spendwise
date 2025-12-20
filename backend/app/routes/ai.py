from fastapi import APIRouter, Depends
from app.services.ai_service import AIService
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI Advisor"])


@router.get("/advice")
async def get_financial_advice(
    query: str = "Give me a summary of my spending",
    current_user: User = Depends(get_current_user),
):
    service = AIService()
    advice = await service.get_advice(current_user.id, query)
    return {"advice": advice}
