from sqlmodel import SQLModel, Field
from typing import Optional


class MovieBase(SQLModel):
    title: str
    director: str
    year: int
    rating: Optional[float] = None


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id: int


class MovieUpdate(SQLModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None
    rating: float | None = None
