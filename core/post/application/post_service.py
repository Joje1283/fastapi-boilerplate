from ulid import ULID
from datetime import datetime
from core.post.application.schema.post import PostCommand, PostsQuery
from core.post.domain.post import Post, Tag
from common.decorator.db_scope import query_handler, command_handler
from core.infra.cache import cached
from common.unit_of_work.uow import AbcUnitOfWork


class PostQueryService:
    def __init__(
        self,
        read_uow: AbcUnitOfWork,
        ulid: ULID,
    ):
        self.uow = read_uow
        self.ulid = ulid

    @query_handler
    async def get_post(self, post_id: str) -> Post:
        return await self.uow.post_repo.find_by_id(id=post_id)

    @query_handler
    @cached(ttl=30)
    async def get_posts(self, posts_query: PostsQuery) -> tuple[int, list[Post]]:
        return await self.uow.post_repo.find_all(
            limit=posts_query.limit,
            offset=posts_query.offset,
            author_id=posts_query.author_id,
            tag_ids=posts_query.tags,
        )


class PostCommandService:
    def __init__(
        self,
        write_uow: AbcUnitOfWork,
        ulid: ULID,
    ):
        self.uow = write_uow
        self.ulid = ulid

    @command_handler
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

    @command_handler
    async def update_post(self, post_id: str, post_command: PostCommand) -> Post:
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
