from sqlmodel import Session
from app.dals.transactions import TransactionDal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, session: Session):
        self.dal = TransactionDal(session)

    def list_user_transactions(self, user_id: int):
        return self.dal.get_all_by_user(user_id)

    def create_user_transaction(
        self, transaction_data: TransactionCreate, user_id: int
    ):
        transaction = Transaction(**transaction_data.model_dump(), user_id=user_id)
        return self.dal.create(transaction)

    def update_user_transaction(
        self, transaction_id: int, transaction_data: TransactionUpdate, user_id: int
    ):
        transaction = self.dal.get_by_id(transaction_id, user_id)
        if not transaction:
            return None

        for field, value in transaction_data.model_dump(exclude_unset=True).items():
            setattr(transaction, field, value)

        return self.dal.update(transaction)

    def delete_user_transaction(self, transaction_id: int, user_id: int):
        transaction = self.dal.get_by_id(transaction_id, user_id)
        if not transaction:
            return False

        self.dal.delete(transaction)
        return True
