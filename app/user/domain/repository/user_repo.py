from abc import ABCMeta, abstractmethod
from app.user.domain.user import User


class AbcUserRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> None:
        raise NotImplementedError
