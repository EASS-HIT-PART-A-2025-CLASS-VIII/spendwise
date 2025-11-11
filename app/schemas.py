from pydantic import BaseModel, ConfigDict
from typing import Optional


class MovieBase(BaseModel):
    title: str
    director: str
    year: int
    rating: Optional[float] = None


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    model_config = ConfigDict(from_attributes=True)