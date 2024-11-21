import logging
from redis import asyncio as aioredis
from core.redis.config import REDIS_SETTINGS, REDIS_DBS

logger = logging.getLogger(__name__)

class RedisFactory:
    def __init__(self):
        self.redis_pools = {}

    def create_redis_pool(self, name: str, db: int) -> aioredis.Redis:
        if name not in self.redis_pools:
            try:
                pool = aioredis.Redis(
                    host=REDIS_SETTINGS['host'],
                    port=REDIS_SETTINGS['port'],
                    password=REDIS_SETTINGS.get('password'),
                    db=db,
                    ssl=REDIS_SETTINGS.get('ssl'),
                    ssl_ca_certs=REDIS_SETTINGS.get('certificate_authority'),
                    encoding=REDIS_SETTINGS.get('encoding', 'utf-8'),
                    decode_responses=REDIS_SETTINGS.get('decode_responses', True),
                    max_connections=REDIS_SETTINGS.get('max_connections', 10)
                )
                self.redis_pools[name] = pool
                logger.debug(f"Created Redis pool '{name}' with DB {db}.")
            except Exception as e:
                logger.error(f"Failed to create Redis pool '{name}': {e}")
                raise
        else:
            logger.debug(f"Redis pool '{name}' already exists.")
        return self.redis_pools[name]

    async def get_redis_pool(self, name: str) -> aioredis.Redis:
        pool = self.redis_pools.get(name)
        if pool is None:
            logger.error(f"Redis pool '{name}' not found.")
            raise ValueError(f"No Redis pool found for '{name}'")
        logger.debug(f"Retrieved Redis pool '{name}'.")
        return pool

redis_factory = RedisFactory()

async def init_redis_pools():
    for name, db in REDIS_DBS.items():
        redis_factory.create_redis_pool(name, db)
    logger.debug("All Redis pools have been initialized.")
