from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import get_settings


settings = get_settings()


class Container(containers.DeclarativeContainer):
    engine = providers.Singleton(create_async_engine, settings.sqlalchemy_database_url, echo=True)
    session = providers.Factory(sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False)
