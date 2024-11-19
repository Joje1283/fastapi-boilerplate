from abc import ABCMeta, abstractmethod
from app.user.domain.repository.user_repo import AbcUserRepository


class AbcUnitOfWork(metaclass=ABCMeta):
    user_repo: AbcUserRepository

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError
