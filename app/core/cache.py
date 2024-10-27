import os
import redis.asyncio as aioredis

# Initialize Redis client using environment variable or default localhost URL
redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
