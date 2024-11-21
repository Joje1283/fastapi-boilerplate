from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import async_engine, async_read_engine


async def get_session_for_container() -> AsyncSession:
    """
    Returns a new session without automatic transaction management.
    """
    session = AsyncSession(async_engine)
    return session


async def get_read_session_for_container() -> AsyncSession:
    """
    Returns a new session without automatic transaction management.
    """
    session = AsyncSession(async_read_engine)
    return session
