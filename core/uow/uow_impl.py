from app.user.infra.repository.user_repo import UserRepository
from core.uow.abstract import AbcUnitOfWork


class UnitOfWork(AbcUnitOfWork):
    def __init__(self):
        self.user_repo = UserRepository()
