from dependency_injector import containers, providers
from ulid import ULID

from core.application.service.auth_service import AuthService
from core.application.service.post_service import PostCommandService, PostQueryService
from core.application.service.user_service import UserCommandService, UserQueryService
from common.config import get_settings
from core.infra.database import get_read_session, get_session
from core.infra.unit_of_work.uow import UnitOfWork
from utils.hashing import Crypto

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["core", "utils"])
    session_provider = providers.Factory(get_session)
    read_session_provider = providers.Factory(get_read_session)
    write_uow = providers.Factory(UnitOfWork, session=session_provider)
    read_uow = providers.Factory(UnitOfWork, session=read_session_provider)
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)
    auth_service = providers.Factory(AuthService)
    user_command_service = providers.Factory(UserCommandService, crypto=crypto, write_uow=write_uow, ulid=ulid)
    user_query_service = providers.Factory(
        UserQueryService, crypto=crypto, read_uow=read_uow, auth_service=auth_service
    )
    post_command_service = providers.Factory(PostCommandService, write_uow=write_uow, ulid=ulid)
    post_query_service = providers.Factory(PostQueryService, read_uow=read_uow, ulid=ulid)
