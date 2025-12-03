from typing import Optional
from sqlmodel import SQLModel, Field


# Define movie model for db table structure.
class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    director: str
    year: int
    rating: Optional[float] = None
