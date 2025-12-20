import asyncio
from arq.connections import RedisSettings


async def generate_monthly_report(ctx, user_id: int):
    await asyncio.sleep(5)
    print(f"Generated PDF report for user {user_id}")


class WorkerSettings:
    functions = [generate_monthly_report]
    redis_settings = RedisSettings(host="redis", port=6379)


if __name__ == "__main__":
    from arq.worker import run_worker

    run_worker(WorkerSettings)
