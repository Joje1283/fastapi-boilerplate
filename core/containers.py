from dependency_injector import containers, providers
from ulid import ULID

from app.user.application.user_service import UserService
from app.user.infra.repository.unit_of_work import UnitOfWork
from core.config import get_settings
from core.dependencies.database import get_session_for_container, get_read_session_for_container
from utils.hashing import Crypto

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app", "core", "utils"])
    session_provider = providers.Factory(get_session_for_container)
    read_session_provider = providers.Factory(get_read_session_for_container)
    uow = providers.Factory(UnitOfWork, session=session_provider)
    read_uow = providers.Factory(UnitOfWork, session=read_session_provider, is_read_only=True)
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)
    user_service = providers.Factory(UserService, ulid=ulid, crypto=crypto)
