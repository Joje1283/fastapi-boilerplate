from dependency_injector import containers, providers
from ulid import ULID

from app.auth.application.auth_service import AuthService
from app.post.application.post_service import PostCommandService, PostQueryService
from app.user.application.user_service import UserService
from core.config import get_settings
from core.database import get_read_session, get_session
from core.uow.uow_impl import UnitOfWork
from utils.hashing import Crypto

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app", "core", "utils"])
    session_provider = providers.Factory(get_session)
    read_session_provider = providers.Factory(get_read_session)
    write_uow = providers.Factory(UnitOfWork, session=session_provider)
    read_uow = providers.Factory(UnitOfWork, session=read_session_provider)
    ulid = providers.Factory(ULID)
    crypto = providers.Factory(Crypto)
    auth_service = providers.Factory(AuthService)
    user_service = providers.Factory(UserService, ulid=ulid, crypto=crypto, uow=write_uow, auth_service=auth_service)
    post_command_service = providers.Factory(PostCommandService, write_uow=write_uow, ulid=ulid)
    post_query_service = providers.Factory(PostQueryService, read_uow=read_uow, ulid=ulid)
