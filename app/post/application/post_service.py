from ulid import ULID
from datetime import datetime

from app.post.application.schema.post import PostCommand, PostsQuery
from app.post.domain.post import Post, Tag
from core.uow.abstract import AbcUnitOfWork


class PostService:
    def __init__(
        self,
        uow: AbcUnitOfWork,
        ulid: ULID,
    ):
        self.uow = uow
        self.ulid = ulid

    async def create_post(self, post_command: PostCommand) -> Post:
        now = datetime.now()
        await self.uow.post_repo.save(
            Post(
                id=self.ulid.generate(),
                title=post_command.title,
                content=post_command.content,
                author_id=post_command.user_id,
                tags=[
                    Tag(
                        id=self.ulid.generate(),
                        name=tag_name,
                    )
                    for tag_name in post_command.tags
                ],
                created_at=now,
                updated_at=now,
            )
        )

    async def get_post(self, post_id: int) -> Post:
        pass

    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        pass
