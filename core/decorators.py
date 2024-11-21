import sys
from functools import wraps


def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        uow = kwargs.get("uow")
        if not uow:
            raise ValueError("uow is required.")
        async with uow:  # 컨텍스트 매니저로 uow 사용
            return await func(*args, **kwargs)

    return wrapper
