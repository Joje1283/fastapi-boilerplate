from app.post.domain.post import Post
from app.post.domain.repository.post_repo import AbcPostRepository


class PostRepository(AbcPostRepository):
    async def save(self, post: Post):
        pass

    async def find_by_id(self, post_id: int) -> Post:
        pass

    async def find_all(self) -> list[Post]:
        pass

    async def delete(self, post_id: int):
        pass
