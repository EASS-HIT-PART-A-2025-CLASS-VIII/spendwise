from sqlmodel import SQLModel, Field
from typing import Optional


class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    director: str
    year: int
    rating: Optional[float] = None
