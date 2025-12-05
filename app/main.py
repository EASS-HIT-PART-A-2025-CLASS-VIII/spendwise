from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes.movies import router as movies_router
from contextlib import asynccontextmanager


app = FastAPI(title="🎬 Movie Catalogue API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() # Or connect to external services
    yield

app = FastAPI(lifespan=lifespan)


# Include movie router
app.include_router(movies_router)
