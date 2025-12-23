import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import create_db_and_tables
from app.routes import auth, transactions, ai
from contextlib import asynccontextmanager

# Simple, clean path at the root of your backend folder
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="💰 SpendWise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use the simplified path
app.mount("/reports-files", StaticFiles(directory=DATA_DIR), name="data")

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(ai.router)
