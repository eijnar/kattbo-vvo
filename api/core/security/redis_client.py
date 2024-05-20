import logging

from redis import asyncio as aioredis

from core.config import settings

logger = logging.getLogger('__name__')
redis_pools = {}

async def init_redis_pools():
    redis_pools['tokens'] = aioredis.Redis(
        host=settings.REDIS_HOSTNAME,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_TOKEN_DB,
        ssl=settings.REDIS_SSL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=10  # Adjust pool size as needed
    )
    redis_pools['unconfirmed_users'] = aioredis.Redis(
        host=settings.REDIS_HOSTNAME,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_UNCONFIRMED_USER_DB,
        ssl=settings.REDIS_SSL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=10  # Adjust pool size as needed
    )


async def get_redis_pool(pool_name: str) -> aioredis.Redis:
    return redis_pools.get(pool_name)


async def get_redis_client_for_tokens() -> aioredis.Redis:
    return await get_redis_pool('tokens')


async def get_redis_client_for_unconfirmed_users() -> aioredis.Redis:
    return await get_redis_pool('unconfirmed_users')
