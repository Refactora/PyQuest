"""Redis клієнт для кешування сесій та rate limiting."""
import json
from typing import Optional, Any

import redis.asyncio as aioredis

from app.core.config import settings

_redis_pool: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_pool


async def redis_set(key: str, value: Any, ttl: int = 7200) -> None:
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=ttl)


async def redis_get(key: str) -> Optional[Any]:
    r = await get_redis()
    data = await r.get(key)
    return json.loads(data) if data else None


async def redis_delete(key: str) -> None:
    r = await get_redis()
    await r.delete(key)


async def redis_incr(key: str, ttl: int = 60) -> int:
    r = await get_redis()
    pipe = r.pipeline()
    await pipe.incr(key)
    await pipe.expire(key, ttl)
    results = await pipe.execute()
    return results[0]
