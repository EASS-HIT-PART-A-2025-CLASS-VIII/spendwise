from __future__ import annotations
from functools import lru_cache
from typing import Any, Optional

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


# ───────────────────────────────
# Settings: loads .env or defaults
# ───────────────────────────────
class UISettings(BaseSettings):
    api_base_url: str = "http://backend:8000"
    trace_id: str = "ui-streamlit"

    model_config = SettingsConfigDict(env_prefix="MOVIE_", env_file=".env", extra="ignore")


settings = UISettings()


# ───────────────────────────────
# Shared HTTP client
# ───────────────────────────────
@lru_cache(maxsize=1)
def _client() -> httpx.Client:
    """Create a single persistent client for performance and header reuse."""
    return httpx.Client(
        base_url=settings.api_base_url,
        headers={"X-Trace-Id": settings.trace_id},
        timeout=5.0,
    )


# ───────────────────────────────
# API functions
# ───────────────────────────────
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
