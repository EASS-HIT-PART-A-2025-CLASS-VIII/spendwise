from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import auth, transactions, ai
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="💰 SpendWise API")

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(ai.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
