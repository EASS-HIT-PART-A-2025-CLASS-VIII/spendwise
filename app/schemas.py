from pydantic import BaseModel, ConfigDict
from typing import Optional

# Define all types and dtos to be used in the endpoints and services.


class MovieBase(BaseModel):
    title: str
    director: str
    year: int
    rating: Optional[float] = None


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
