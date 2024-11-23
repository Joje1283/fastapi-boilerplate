from functools import wraps
from core.database import session


def transactional(func):
    @wraps(func)
    async def _transactional(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

        return result

    return _transactional
