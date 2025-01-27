import functools
import pickle
import hashlib
import json
from core.infra.redis import redis_client as cache_client
from core.infra.logger import logger


def is_serializable(value):
    try:
        json.dumps(value)  # Check if JSON serializable
        return True
    except (TypeError, ValueError):
        return False


def cached(
    ttl: int = 600,
):
    """
    Cache Decorator
    :param ttl: Cache expiration time

    @cached() # Cache expiration time 600 seconds
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Generate cache key
                serializable_args = [arg for arg in args if is_serializable(arg)]
                serializable_kwargs = {k: v for k, v in kwargs.items() if is_serializable(v)}

                hash_input = f"{serializable_args}:{serializable_kwargs}"
                hs = hashlib.md5(hash_input.encode("utf-8")).hexdigest()

                if serializable_args or serializable_kwargs:
                    hash_key = f"{func.__module__}.{func.__name__}:{hs}"
                else:
                    hash_key = f"{func.__module__}.{func.__name__}"
                cached_data = await cache_client.get(hash_key)
                if cached_data:
                    result = pickle.loads(cached_data)
                    return result
                result = await func(*args, **kwargs)
                cache_data = pickle.dumps(result)
                await cache_client.set(hash_key, cache_data, ttl)
            except Exception as e:
                result = await func(*args, **kwargs)
                logger.error(e)
            return result

        return wrapper

    return decorator
