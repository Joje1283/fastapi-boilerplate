import redis.asyncio as redis
from common.config import get_settings

settings = get_settings()
RedisClient = redis.Redis
redis_client: RedisClient = redis.Redis(host=settings.redis_url, port=6379, socket_timeout=10)
