from sqlmodel.ext.asyncio.session import AsyncSession

from app.post.infra.repository.post_repo import PostRepository
from app.post.infra.repository.tag_repo import TagRepository
from app.user.infra.repository.user_repo import UserRepository
from core.uow.abstract import AbcUnitOfWork


class UnitOfWork(AbcUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session=self.session)
        self.post_repo = PostRepository(session=self.session)
        self.tag_repo = TagRepository(session=self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()
