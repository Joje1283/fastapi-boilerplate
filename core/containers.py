from dependency_injector import containers, providers
from ulid import ULID

from app.user.application.user_service import UserService
from app.user.infra.repository.unit_of_work import UnitOfWork
from core.config import get_settings
from utils.hashing import Crypto

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app", "core", "utils"])
    uow = providers.Factory(UnitOfWork)
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)
    user_service = providers.Factory(UserService, ulid=ulid, crypto=crypto, uow=uow)
