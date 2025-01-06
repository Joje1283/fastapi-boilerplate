import time
from asyncio import sleep
from functools import wraps
from typing import Callable, Any
from asyncio import iscoroutinefunction
from core.infra.redis import redis_client
from core.infra.redis import RedisClient

PREFIX = "distributed_lock:{key}"


async def release_lock(client: RedisClient, key: str):
    return await client.delete(PREFIX.format(key=key))


async def acquire_lock(client: RedisClient, key: str, lock_timeout: int = 10, acquire_timeout: int = 10):
    lock_key = PREFIX.format(key=key)
    end = time.time() + acquire_timeout
    while time.time() < end:
        if await client.set(lock_key, "lock", lock_timeout, nx=True):
            return True
        await sleep(0.1)
        print(f"Failed to acquire lock for key: {key}")
    return False


def distributed_lock(
    key_template: str,
    lock_timeout: int = 10,
    acquire_timeout: int = 10,
):
    """
    Decorator that provides distributed locks

    :param key_template: lock key template (예: "draw_winner:{draw_item_id}")
    :param lock_timeout: lock expiration time (seconds)
    :param acquire_timeout: lock acquisition waiting time (seconds)
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = key_template.format(**kwargs)
            if await acquire_lock(
                client=redis_client, key=key, lock_timeout=lock_timeout, acquire_timeout=acquire_timeout
            ):
                try:
                    if iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)
                finally:
                    await release_lock(client=redis_client, key=key)
            else:
                raise TimeoutError(f"Failed to acquire lock for key: {key}")

        return wrapper

    return decorator
