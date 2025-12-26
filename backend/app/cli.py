import csv
import typer
from datetime import datetime
from sqlmodel import Session, select, delete
from app.database import engine, create_db_and_tables
from app.models.transaction import Transaction
from app.models.user import User
from app.core.security import get_password_hash

app = typer.Typer(help="SpendWise CLI: Manage financial telemetry and users.")


@app.command()
def seed():
    """Create tables, ensure a default user exists, and seed transactions."""
    # 1. Automatically create tables if they don't exist
    create_db_and_tables()

    csv_path = "app/data/transactions.csv"

    with Session(engine) as session:
        # 2. Check for the default user or create one
        statement = select(User).where(User.username == "john")
        db_user = session.exec(statement).first()

        if not db_user:
            typer.echo("👤 Default user 'john' not found. Creating now...")
            db_user = User(
                username="john",
                hashed_password=get_password_hash("password123"),
                role="user",
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

        # 3. Seed transactions from CSV
        transactions = []
        try:
            with open(csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    transactions.append(
                        Transaction(
                            amount=float(row["amount"]),
                            category=row["category"],
                            description=row["description"],
                            date=datetime.fromisoformat(row["date"]),
                            user_id=db_user.id,
                        )
                    )

            session.add_all(transactions)
            session.commit()
            typer.echo(
                f"🚀 Seeded {len(transactions)} transactions for user {db_user.username}"
            )
        except FileNotFoundError:
            typer.echo(f"❌ Error: CSV file not found at {csv_path}")


@app.command()
def list():
    """List all financial transactions currently in the database."""
    with Session(engine) as session:
        result = session.exec(select(Transaction)).all()
        if not result:
            typer.echo("No transactions found.")
            raise typer.Exit()

        typer.echo(f"{'ID':<4} | {'Amount':<10} | {'Category':<15} | {'Description'}")
        typer.echo("-" * 60)
        for t in result:
            typer.echo(
                f"{t.id:<4} | ${t.amount:<9} | {t.category:<15} | {t.description}"
            )


@app.command()
def reset():
    """Delete all transactions from the database."""
    with Session(engine) as session:
        session.execute(delete(Transaction))
        session.commit()
        typer.echo("🧹 Database Reset: Deleted transactions.")


if __name__ == "__main__":
    app()
