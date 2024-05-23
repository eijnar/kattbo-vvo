from redis import asyncio as aioredis
from core.redis.config import REDIS_SETTINGS, REDIS_DBS

class RedisFactory:
    def __init__(self):
        self.redis_pools = {}

    def create_redis_pool(self, name, db):
        if name not in self.redis_pools:
            self.redis_pools[name] = aioredis.Redis(
                host=REDIS_SETTINGS['host'],
                port=REDIS_SETTINGS['port'],
                password=REDIS_SETTINGS['password'],
                db=db,
                ssl=REDIS_SETTINGS['ssl'],
                encoding=REDIS_SETTINGS['encoding'],
                decode_responses=REDIS_SETTINGS['decode_responses'],
                max_connections=REDIS_SETTINGS['max_connections']
            )
        return self.redis_pools[name]

    async def get_redis_pool(self, name: str) -> aioredis.Redis:
        return self.redis_pools.get(name)

# Initialize the Redis factory
redis_factory = RedisFactory()

async def init_redis_pools():
    for name, db in REDIS_DBS.items():
        redis_factory.create_redis_pool(name, db)
