from ulid import ULID
from datetime import datetime
from app.post.application.schema.post import PostCommand, PostsQuery
from app.post.domain.post import Post, Tag
from core.decorators import transactional
from core.uow.abstract import AbcUnitOfWork


class PostService:
    def __init__(
        self,
        uow: AbcUnitOfWork,
        ulid: ULID,
    ):
        self.uow = uow
        self.ulid = ulid

    @transactional
    async def create_post(self, post_command: PostCommand) -> Post:
        now = datetime.now()
        return await self.uow.post_repo.save(
            Post(
                id=self.ulid.generate(),
                title=post_command.title,
                contents=post_command.contents,
                author_id=post_command.author_id,
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
        async with self.uow:
            return await self.uow.post_repo.find_by_id(id=post_id)

    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        return await self.uow.post_repo.find_all(
            limit=posts_query.limit,
            offset=posts_query.offset,
            author_id=posts_query.author_id,
            tag_ids=posts_query.tags,
        )

    async def update_post(self, post_id: str, post_command: PostCommand) -> Post:
        async with self.uow:
            post: Post = await self.uow.post_repo.find_by_id(id=post_id)
            if post_command.author_id is not None:
                post.author_id = post_command.author_id
            if post_command.title is not None:
                post.title = post_command.title
            if post_command.contents is not None:
                post.contents = post_command.contents
            if post_command.tags is not None:
                post.tags = [
                    Tag(
                        id=self.ulid.generate(),
                        name=tag_name,
                    )
                    for tag_name in post_command.tags
                ]
            post.updated_at = datetime.now()
            return await self.uow.post_repo.update(
                id=post_id,
                post_vo=post,
            )
