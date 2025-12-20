from sqlmodel import Session, select
from typing import List, Optional
from app.models.transaction import Transaction


class TransactionDal:
    def __init__(self, session: Session):
        self.session = session

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
