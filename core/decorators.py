from functools import wraps


def db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        uow = kwargs.get("uow")
        if not uow:
            raise ValueError("uow is required.")
        async with uow:
            return await func(*args, **kwargs)

    return wrapper
