from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.domain.repository.unit_of_work import AbcUnitOfWork
from app.user.infra.repository.user_repo import UserRepository


class UnitOfWork(AbcUnitOfWork):
    def __init__(self, session: AsyncSession, is_read_only: bool = False):
        self.session = session
        self.is_read_only = is_read_only
        self.user_repo = UserRepository(session=session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.is_read_only:
            if exc_type is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        await self.session.close()
