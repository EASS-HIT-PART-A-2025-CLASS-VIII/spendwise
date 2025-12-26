import pytest
import asyncio
from scripts.refresh import refresh_user_analysis
import redis.asyncio as redis


@pytest.mark.anyio
async def test_refresh_idempotency():
    # Inside Docker, the hostname is 'redis' not 'localhost'
    r = redis.from_url("redis://redis:6379")
    sem = asyncio.Semaphore(1)
    user_id = 999

    await r.delete(f"refresh_lock:user:{user_id}")
    await r.set(f"refresh_lock:user:{user_id}", "done")

    # This should return immediately without making an HTTP call
    result = await refresh_user_analysis(user_id, r, sem)
    assert result is None

    await r.delete(f"refresh_lock:user:{user_id}")
    await r.aclose()
