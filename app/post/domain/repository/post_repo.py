from abc import ABCMeta, abstractmethod

from app.post.domain.post import Post


class AbcPostRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, post: Post):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, post_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, post_id: int):
        raise NotImplementedError
