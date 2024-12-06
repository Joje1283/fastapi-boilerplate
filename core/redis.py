import redis.asyncio as redis
from core.config import get_settings

settings = get_settings()
redis_client = redis.Redis(host=settings.redis_url, port=6379, socket_timeout=10)
