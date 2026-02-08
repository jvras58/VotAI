"""Redis client configuration."""

import redis

from app.utils.settings import get_settings


def get_redis_client() -> redis.Redis:
    """Get the Redis client instance."""
    return redis.Redis(
        host=get_settings().REDIS_HOST,
        port=get_settings().REDIS_PORT,
    )


redis_client = get_redis_client()
