import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from arq import create_pool
from arq.connections import RedisSettings

from app.database import get_session
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionRead,
    TransactionUpdate,
)
from app.services.transactions import TransactionService
from app.core.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/stats/detailed")
def get_detailed_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(session).get_dashboard_stats(current_user.id)


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


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    updated = TransactionService(session).update_user_transaction(
        transaction_id, transaction_data, current_user.id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated


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


@router.post("/report")
async def trigger_report(current_user: User = Depends(get_current_user)):
    redis = await create_pool(RedisSettings(host="redis", port=6379))
    await redis.enqueue_job("generate_monthly_report", current_user.id)
    return {"message": "Report generation started in background"}


@router.get("/report/list")
def list_reports(current_user: User = Depends(get_current_user)):
    path = "data"
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".pdf")]
