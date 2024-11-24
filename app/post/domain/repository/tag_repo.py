from abc import ABCMeta


class AbcTagRepository(metaclass=ABCMeta):
    def save(self, tags: list[str]):
        raise NotImplementedError

    def delete(self, tag_ids: list[int]):
        raise NotImplementedError
