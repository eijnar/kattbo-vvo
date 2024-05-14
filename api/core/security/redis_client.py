from redis import asyncio as aioredis

from core.config import settings


redis_client = None

async def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            ssl=settings.REDIS_SSL,
            encoding="utf-8"
        )
    return await redis_client