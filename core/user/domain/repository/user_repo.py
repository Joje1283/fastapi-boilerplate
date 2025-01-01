from abc import ABCMeta, abstractmethod
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from core.user.domain.user import User


class AbcUserRepository(metaclass=ABCMeta):
    session: AsyncSession

    @abstractmethod
    async def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: EmailStr) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> None:
        raise NotImplementedError
