from abc import ABCMeta, abstractmethod

from app.post.domain.post import Post
from app.post.domain.repository.tag_repo import AbcTagRepository


class AbcPostRepository(metaclass=ABCMeta):
    tag_repository: AbcTagRepository

    @abstractmethod
    async def save(self, post: Post):
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, post_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: int):
        raise NotImplementedError
