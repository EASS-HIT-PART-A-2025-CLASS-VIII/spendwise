from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.services.transactions_service import TransactionService
from app.core.deps import get_current_user
from arq import create_pool
from arq.connections import RedisSettings
import os

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionRead])
def list_transactions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(session).list_user_transactions(current_user.id)


@router.post("", response_model=TransactionRead)
def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(session).create_user_transaction(
        transaction, current_user.id
    )


@router.post("/report")
async def trigger_report(current_user: User = Depends(get_current_user)):
    redis = await create_pool(RedisSettings(host="redis", port=6379))
    await redis.enqueue_job("generate_monthly_report", current_user.id)
    return {"message": "Report generation started in background"}


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    success = TransactionService(session).delete_user_transaction(
        transaction_id, current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}


@router.get("/report/list")
def list_reports(current_user: str = Depends(get_current_user)):
    path = "data"
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".pdf")]
