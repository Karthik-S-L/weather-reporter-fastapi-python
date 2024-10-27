import redis.asyncio as aioredis
import os

# Initialize Redis client
redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

async def get_cache(key: str):
    return await redis.get(key)

async def set_cache(key: str, value: str, expire: int = 3600):
    await redis.set(key, value, ex=expire)
