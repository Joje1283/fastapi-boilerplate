from abc import ABCMeta

from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.domain.repository.user_repo import AbcUserRepository


class AbcUnitOfWork(metaclass=ABCMeta):
    user_repo: AbcUserRepository

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, *args):
        raise NotImplementedError
