from core.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine

settings = get_settings()

async_engine = create_async_engine(
    settings.sqlalchemy_database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=12,
    pool_timeout=10,
)

async_read_engine = create_async_engine(
    settings.sqlalchemy_database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=12,
    pool_timeout=10,
)
