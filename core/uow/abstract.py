from abc import ABCMeta

from app.post.domain.repository.post_repo import AbcPostRepository
from app.post.domain.repository.tag_repo import AbcTagRepository
from app.user.domain.repository.user_repo import AbcUserRepository


class AbcUnitOfWork(metaclass=ABCMeta):
    user_repo: AbcUserRepository
    post_repo: AbcPostRepository
    tag_repo: AbcTagRepository
