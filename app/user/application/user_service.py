from dependency_injector.wiring import Provide
from fastapi import HTTPException
from starlette import status
from ulid import ULID
from datetime import datetime

from app.user.application.schema.user import RegisterUserCommand, LoginQuery
from app.user.domain.repository.unit_of_work import AbcUnitOfWork
from app.user.domain.user import User, Profile
from common.constants import Role
from core.decorators import transactional
from utils.hashing import Crypto
from utils.jwt_utils import create_access_token


class UserService:
    def __init__(
        self,
        ulid: ULID,
        crypto: Crypto,
    ):
        self.ulid = ulid
        self.crypto = crypto

    @transactional
    async def register_user(
        self,
        register_command: RegisterUserCommand,
        uow: AbcUnitOfWork = Provide["uow"],
    ) -> User:
        user = await uow.user_repo.find_by_email(email=register_command.email)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        now = datetime.now()
        return await uow.user_repo.save(
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

    @transactional
    async def login(
        self,
        login_query: LoginQuery,
        uow: AbcUnitOfWork = Provide["uow"],
    ):
        user: User = await uow.user_repo.find_by_email(login_query.email)
        if not self.crypto.verify(login_query.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = create_access_token(payload={"user_id": user.id}, role=Role.USER)
        return access_token
