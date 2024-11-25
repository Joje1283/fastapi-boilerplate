from app.post.domain.post import Post
from app.post.domain.repository.post_repo import AbcPostRepository


class PostRepository(AbcPostRepository):
    async def save(self, post: Post) -> Post:
        pass

    async def find_by_id(self, id: int) -> Post:
        pass

    async def find_all(
        self, limit: int, offset: int, tag_ids: list[int], author_id: int = None
    ) -> tuple[int, list[Post]]:
        pass

    async def delete(self, post_id: int):
        pass
