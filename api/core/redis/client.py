# core/redis/client.py

import logging
from redis import asyncio as aioredis
from fastapi import HTTPException, status
from core.redis.factory import redis_factory

logger = logging.getLogger(__name__)

async def get_redis_client(pool_name: str) -> aioredis.Redis:
    """
    Generic function to retrieve a Redis client by pool name.

    Args:
        pool_name (str): The name of the Redis pool.

    Returns:
        aioredis.Redis: The Redis client.

    Raises:
        HTTPException: If the Redis pool is not found or an unexpected error occurs.
    """
    try:
        client = await redis_factory.get_redis_pool(pool_name)
        logger.debug(f"Obtained Redis client for pool '{pool_name}'.")
        return client
    except ValueError as ve:
        logger.error(f"Error getting Redis client for pool '{pool_name}': {ve}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while accessing cache."
        )
    except Exception as e:
        logger.error(f"Unexpected error getting Redis client for pool '{pool_name}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while accessing cache."
        )

# Specific client getters using the generic get_redis_client
async def get_redis_client_for_tokens() -> aioredis.Redis:
    return await get_redis_client('tokens')

async def get_redis_client_for_authorize() -> aioredis.Redis:
    return await get_redis_client('authorize')

async def get_redis_client_for_unconfirmed_users() -> aioredis.Redis:
    return await get_redis_client('unconfirmed_users')

async def get_redis_client_for_cache() -> aioredis.Redis:
    return await get_redis_client('cache')