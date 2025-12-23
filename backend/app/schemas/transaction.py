from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class TransactionBase(SQLModel):
    amount: float
    category: str
    description: str
    date: datetime


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    category: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime] = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
