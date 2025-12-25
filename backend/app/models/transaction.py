from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    category: str
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
