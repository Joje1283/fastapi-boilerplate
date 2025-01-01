from contextvars import ContextVar
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from common.config import get_settings

config = get_settings()

session_context: ContextVar[str] = ContextVar("session_context")


async_engine = create_async_engine(
    config.sqlalchemy_database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=12,
    pool_timeout=10,
)

async_read_engine = create_async_engine(
    config.sqlalchemy_database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=12,
    pool_timeout=10,
)


async def get_session() -> AsyncSession:
    """
    Returns a new session without automatic transaction management.
    """
    return AsyncSession(async_engine)


async def get_read_session() -> AsyncSession:
    """
    Returns a new session without automatic transaction management.
    """
    return AsyncSession(async_read_engine)
