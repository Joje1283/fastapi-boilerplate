from abc import ABCMeta, abstractmethod


class AbcTagRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, tags: list[str]):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, tag_ids: list[int]):
        raise NotImplementedError
