from sqlmodel import Session, select
from typing import Optional, List
from app.models.transaction import Transaction
from sqlalchemy import func
from datetime import datetime, timedelta


class TransactionDal:
    def __init__(self, session: Session):
        self.session = session

    def get_monthly_total(self, user_id: int, start_date: datetime) -> float:
        result = (
            self.session.query(func.sum(Transaction.amount))
            .filter(Transaction.user_id == user_id, Transaction.date >= start_date)
            .scalar()
        )
        return float(result) if result else 0.0

    def get_category_breakdown(self, user_id: int) -> List:
        return (
            self.session.query(
                Transaction.category, func.sum(Transaction.amount).label("total")
            )
            .filter(Transaction.user_id == user_id)
            .group_by(Transaction.category)
            .all()
        )

    def get_daily_spending(self, user_id: int, days: int = 30):
        start_date = datetime.now() - timedelta(days=days)
        # Grouping by date helps create the points for the chart
        return (
            self.session.query(
                func.date(Transaction.date).label("day"),
                func.sum(Transaction.amount).label("total"),
            )
            .filter(Transaction.user_id == user_id, Transaction.date >= start_date)
            .group_by(func.date(Transaction.date))
            .order_by(func.date(Transaction.date))
            .all()
        )

    def get_all_by_user(self, user_id: int) -> List[Transaction]:
        return self.session.exec(
            select(Transaction).where(Transaction.user_id == user_id)
        ).all()

    def get_by_id(self, transaction_id: int, user_id: int) -> Optional[Transaction]:
        return self.session.exec(
            select(Transaction).where(
                Transaction.id == transaction_id, Transaction.user_id == user_id
            )
        ).first()

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def update(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction):
        self.session.delete(transaction)
        self.session.commit()
