from abc import ABCMeta

from core.domain.repository.post_repo import AbcPostRepository
from core.domain.repository.tag_repo import AbcTagRepository
from core.domain.repository.user_repo import AbcUserRepository


class AbcUnitOfWork(metaclass=ABCMeta):
    user_repo: AbcUserRepository
    post_repo: AbcPostRepository
    tag_repo: AbcTagRepository

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError
