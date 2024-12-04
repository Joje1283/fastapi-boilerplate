from functools import wraps


def transactional(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
