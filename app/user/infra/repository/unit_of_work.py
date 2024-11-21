from app.user.domain.repository.unit_of_work import AbcUnitOfWork
from app.user.infra.repository.user_repo import UserRepository


class UnitOfWork(AbcUnitOfWork):
    def __init__(self):
        self.user_repo = UserRepository()
