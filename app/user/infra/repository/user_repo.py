from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.domain.repository.user_repo import AbcUserRepository
from app.user.domain.user import User as UserEntity


class UserRepository(AbcUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserEntity) -> UserEntity:
        pass

    async def find_by_email(self, email: str) -> UserEntity:
        pass

    async def delete(self) -> None:
        pass
