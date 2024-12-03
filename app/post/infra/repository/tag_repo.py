from sqlmodel.ext.asyncio.session import AsyncSession

from app.post.domain.repository.tag_repo import AbcTagRepository


class TagRepository(AbcTagRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, tags: list[str]):
        pass

    async def delete(self, tag_ids: list[int]):
        pass
