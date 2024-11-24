from app.post.domain.repository.tag_repo import AbcTagRepository


class TagRepository(AbcTagRepository):
    async def save(self, tags: list[str]):
        pass

    async def delete(self, tag_ids: list[int]):
        pass
