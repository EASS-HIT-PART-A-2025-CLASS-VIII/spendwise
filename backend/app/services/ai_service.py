from pydantic_ai import Agent, RunContext
from sqlmodel import Session, select
from app.models.transaction import Transaction
from app.database import engine

advisor_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt=(
        "You are a professional financial advisor for SpendWise. "
        "Analyze the user's spending habits and provide advice. "
        "Use the get_spend_history tool to see their actual data."
    ),
)


@advisor_agent.tool
async def get_spend_history(ctx: RunContext[int]) -> str:
    user_id = ctx.deps
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.user_id == user_id)
        results = session.exec(statement).all()
        if not results:
            return "No transactions found."

        summary = "\n".join(
            [f"- {t.date}: {t.amount} {t.category} ({t.description})" for t in results]
        )
        return f"User Transactions:\n{summary}"


class AIService:
    async def get_advice(self, user_id: int, user_query: str) -> str:
        result = await advisor_agent.run(user_query, deps=user_id)
        return result.data
