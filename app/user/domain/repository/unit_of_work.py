from abc import ABCMeta
from app.user.domain.repository.user_repo import AbcUserRepository


class AbcUnitOfWork(metaclass=ABCMeta):
    user_repo: AbcUserRepository
