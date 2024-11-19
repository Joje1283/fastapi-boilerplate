from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ulid import ULID

from app.user.application.user_service import UserService
from app.user.infra.repository.unit_of_work import UnitOfWork
from core.config import get_settings
from utils.hashing import Crypto

settings = get_settings()


class Container(containers.DeclarativeContainer):
    engine = providers.Singleton(create_async_engine, settings.sqlalchemy_database_url, echo=True)
    session = providers.Factory(sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False)
    uow = providers.Factory(UnitOfWork, session=session)
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)
    user_service = providers.Factory(UserService, uow=uow, ulid=ulid, crypto=crypto)
