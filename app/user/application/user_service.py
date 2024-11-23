from fastapi import HTTPException
from starlette import status
from ulid import ULID
from datetime import datetime

from app.auth.application.auth_service import AuthService
from app.auth.domain.token import Token
from app.user.application.schema.user import RegisterUserCommand, LoginQuery
from core.uow.abstract import AbcUnitOfWork
from app.user.domain.user import User, Profile
from utils.hashing import Crypto


class UserService:
    def __init__(
        self,
        ulid: ULID,
        crypto: Crypto,
        uow: AbcUnitOfWork,
        auth_service: AuthService,
    ):
        self.ulid = ulid
        self.crypto = crypto
        self.uow = uow
        self.auth_service = auth_service

    async def register_user(
        self,
        register_command: RegisterUserCommand,
    ) -> User:
        user = await self.uow.user_repo.find_by_email(email=register_command.email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        now = datetime.now()
        return await self.uow.user_repo.save(
            User(
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
        )

    async def login(
        self,
        login_query: LoginQuery,
    ) -> Token:
        user: User = await self.uow.user_repo.find_by_email(login_query.email)
        if not self.crypto.verify(login_query.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return await self.auth_service.generate_tokens(user_id=user.id)
