import time
import uuid
import redis.asyncio as redis
from fastapi import Request, HTTPException, status

r = redis.Redis(host='redis', port=6379, decode_responses=True)

RATE_LIMITS = {
    "anonymous": (2, 60),
    "authenticated": (10, 60),
}

async def rate_limit(request: Request, user_id: str | None = None):
    identity = user_id or request.client.host
    limit_type = "authenticated" if user_id else "anonymous"
    limit, period = RATE_LIMITS[limit_type]

    key = f"rate_limit:{identity}"
    now = time.time()
    window_start = now - period

    await r.zremrangebyscore(key, 0, window_start)
    
    request_count = await r.zcard(key)

    if request_count >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

    await r.zadd(key, {f"{now}:{uuid.uuid4()}": now})
    await r.expire(key, period)