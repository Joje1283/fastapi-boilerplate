from abc import ABCMeta, abstractmethod

from app.post.domain.post import Post
from app.post.domain.repository.tag_repo import AbcTagRepository


class AbcPostRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, post_vo: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, post_vo: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: str) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self, limit: int, offset: int, tag_ids: list[int], author_id: int = None
    ) -> tuple[int, list[Post]]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: int):
        raise NotImplementedError

    @abstractmethod
    async def _delete_tags(self):
        raise NotImplementedError
