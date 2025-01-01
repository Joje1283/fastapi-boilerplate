from fastapi import HTTPException
from starlette import status
from ulid import ULID
from datetime import datetime

from core.auth.application.auth_service import AuthService
from core.auth.domain.token import Token
from core.user.application.schema.user import RegisterUserCommand, LoginQuery
from common.decorator.db_scope import query_handler, command_handler
from common.uow.abstract import AbcUnitOfWork
from core.user.domain.user import User, Profile
from utils.hashing import Crypto


class UserQueryService:
    def __init__(
        self,
        crypto: Crypto,
        read_uow: AbcUnitOfWork,
        auth_service: AuthService,
    ):
        self.crypto = crypto
        self.uow = read_uow
        self.auth_service = auth_service

    @query_handler
    async def login(
        self,
        login_query: LoginQuery,
    ) -> Token:
        user: User = await self.uow.user_repo.find_by_email(login_query.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not self.crypto.verify(login_query.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await self.auth_service.generate_tokens(user_id=user.id)


class UserCommandService:
    def __init__(
        self,
        crypto: Crypto,
        write_uow: AbcUnitOfWork,
        ulid: ULID,
    ):
        self.crypto = crypto
        self.uow = write_uow
        self.ulid = ulid

    @command_handler
    async def register_user(
        self,
        register_command: RegisterUserCommand,
    ) -> User:
        _user = await self.uow.user_repo.find_by_email(email=register_command.email)
        if _user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        now = datetime.now()
        user: User = User(
            id=self.ulid.generate(),
            email=register_command.email,
            profile=(
                Profile(
                    name=register_command.profile.name,
                    age=register_command.profile.age,
                    phone=register_command.profile.phone,
                )
                if register_command.profile
                else None
            ),
            password=self.crypto.encrypt(register_command.password),
            created_at=now,
            updated_at=now,
        )

        await self.uow.user_repo.save(user=user)
        return user
