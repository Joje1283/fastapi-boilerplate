from app.post.infra.repository.post_repo import PostRepository
from app.post.infra.repository.tag_repo import TagRepository
from app.user.infra.repository.user_repo import UserRepository
from core.uow.abstract import AbcUnitOfWork


class UnitOfWork(AbcUnitOfWork):
    def __init__(self):
        self.user_repo = UserRepository()
        self.post_repo = PostRepository()
        self.tag_repo = TagRepository()
