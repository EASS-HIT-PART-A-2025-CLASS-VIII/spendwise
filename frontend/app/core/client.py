from __future__ import annotations
from functools import lru_cache
from typing import Any
import httpx
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys
import dotenv


dotenv.load_dotenv()


class UISettings(BaseSettings):
    api_base_url: str
    trace_id: str = "ui-streamlit"

    model_config = SettingsConfigDict(
        env_prefix="MOVIE_", env_file=".env", extra="ignore"
    )


try:
    settings = UISettings()
except ValidationError as e:
    print("FATAL ERROR: Configuration failed to load.")
    print(
        "The required environment variable MOVIE_API_BASE_URL (or MOVIE_API_BASE_URL in .env) must be set."
    )
    print(e)
    # Exits the Streamlit application gracefully if configuration fails
    sys.exit(1)


@lru_cache(maxsize=1)
def _client() -> httpx.Client:
    """Create a single persistent client for performance and header reuse."""
    return httpx.Client(
        base_url=settings.api_base_url,
        headers={"X-Trace-Id": settings.trace_id},
        timeout=5.0,
    )


# API functions
def list_movies() -> list[dict[str, Any]]:
    """Fetch all movies from the backend."""
    response = _client().get("/movies")
    response.raise_for_status()
    return response.json()


def create_movie(title: str, director: str, year: int, rating: float) -> dict[str, Any]:
    """Add a new movie."""
    payload = {
        "title": title,
        "director": director,
        "year": year,
        "rating": rating,
    }
    response = _client().post("/movies", json=payload)
    response.raise_for_status()
    return response.json()


def delete_movie(movie_id: int) -> None:
    """Delete a movie by ID."""
    response = _client().delete(f"/movies/{movie_id}")
    response.raise_for_status()
