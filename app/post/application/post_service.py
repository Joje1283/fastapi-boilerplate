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
        return await self.uow.post_repo.save(
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

    async def get_post(self, post_id: str) -> Post:
        return await self.uow.post_repo.find_by_id(id=post_id)

    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        return await self.uow.post_repo.find_all(
            limit=posts_query.limit,
            offset=posts_query.offset,
            tag_ids=[tag_id for tag_id in posts_query.tags],
            author_id=posts_query.author_id,
        )
