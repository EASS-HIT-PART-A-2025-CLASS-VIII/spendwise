import asyncio
import httpx
import redis.asyncio as redis
import os

# Updated to match main.py routing (removed /api/v1)
API_URL = os.getenv("API_URL", "http://spendwise-backend:8000")
REDIS_URL = os.getenv("REDIS_URL", "redis://spendwise-redis:6379")


async def refresh_user_analysis(
    user_id: int, r: redis.Redis, semaphore: asyncio.Semaphore
):
    async with semaphore:
        idempotency_key = f"refresh_lock:user:{user_id}"

        if await r.exists(idempotency_key):
            print(f"⏩ User {user_id} already processed. Skipping.")
            return

        async with httpx.AsyncClient() as client:
            for attempt in range(3):
                try:
                    # AI route prefix is /ai based on your code
                    response = await client.post(
                        f"{API_URL}/ai/analyze", params={"user_id": user_id}
                    )
                    if response.status_code == 200:
                        await r.setex(idempotency_key, 300, "done")
                        print(f"✅ Refreshed User {user_id}")
                        return
                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(2**attempt)


async def main():
    r = redis.from_url(REDIS_URL)
    semaphore = asyncio.Semaphore(5)
    user_ids = [1]
    tasks = [refresh_user_analysis(uid, r, semaphore) for uid in user_ids]
    await asyncio.gather(*tasks)
    await r.aclose()


if __name__ == "__main__":
    asyncio.run(main())
