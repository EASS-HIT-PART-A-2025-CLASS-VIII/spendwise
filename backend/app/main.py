from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes.movies import router as movies_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="🎬 Movie Catalogue API")

app.include_router(movies_router)
