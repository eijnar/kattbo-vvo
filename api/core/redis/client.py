from redis import asyncio as aioredis
from core.redis.factory import redis_factory


async def get_redis_client(pool_name: str):
    pool = await redis_factory.get_redis_pool(pool_name)
    if pool is None:
        raise ValueError(f"No Redis pool found for {pool_name}")
    return pool


async def get_redis_client_for_tokens():
    return await get_redis_client('tokens')


# Example of adding a new client
async def get_redis_client_for_authorize(
    pool_name: str = 'authorize',
) -> aioredis.Redis:
    """Return a Redis client from the pool with the given name.

    Args:
        pool_name (str, optional): The name of the Redis pool to use. Defaults to 'authorize'.

    Returns:
        aioredis.Redis: A Redis client connected to the specified pool.
    """
    return await get_redis_client(pool_name)


async def get_redis_client_for_unconfirmed_users():
    return await get_redis_client('unconfirmed_users')
