from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import selectinload, RelationshipProperty
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.post.domain.post import Post as PostVO
from app.post.infra.model.post import Tag, Post
from app.post.domain.repository.post_repo import AbcPostRepository


class PostRepository(AbcPostRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _delete_tags(self):
        unused_tags_query = await self.session.exec(select(Tag).where(~Tag.posts.any()).select_from(Tag))
        unused_tags = unused_tags_query.all()
        for tag in unused_tags:
            await self.session.delete(tag)

    async def update(self, id: str, post_vo: PostVO) -> PostVO:
        query = await self.session.exec(
            select(Post).options(selectinload(Post.tags)).where(Post.id == id).select_from(Post)
        )
        post: Post = query.one_or_none()
        if not post:
            raise HTTPException(status_code=422)
        post.title = post_vo.title
        post.contents = post_vo.contents
        post.author_id = post_vo.author_id
        tag_names = [tag.name for tag in post_vo.tags]
        tags_query = await self.session.exec(select(Tag).where(Tag.name.in_(tag_names)).select_from(Tag))
        saved_tags = tags_query.all()
        tags: list[Tag] = []
        saved_tags_dict = {tag.name: tag for tag in saved_tags}
        for tag in post_vo.tags:
            if tag.name in saved_tags_dict:
                tags.append(saved_tags_dict[tag.name])
            else:
                tags.append(Tag(id=tag.id, name=tag.name))
        post.tags = tags
        self.session.add(post)
        await self._delete_tags()
        await self.session.flush()
        return PostVO(
            id=post.id,
            title=post.title,
            contents=post.contents,
            author_id=post.author_id,
            tags=[Tag(id=tag.id, name=tag.name) for tag in post.tags],
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    async def save(self, post_vo: PostVO) -> PostVO:
        # Upsert tags
        tag_names = [tag.name for tag in post_vo.tags]
        tags_query = await self.session.exec(select(Tag).where(Tag.name.in_(tag_names)).select_from(Tag))
        saved_tags = tags_query.all()
        tags: list[Tag] = []
        saved_tags_dict = {tag.name: tag for tag in saved_tags}

        for tag in post_vo.tags:
            if tag.name in saved_tags_dict:
                tags.append(saved_tags_dict[tag.name])
            else:
                tags.append(Tag(id=tag.id, name=tag.name))

        new_post = Post(
            id=post_vo.id,
            title=post_vo.title,
            contents=post_vo.contents,
            author_id=post_vo.author_id,
            tags=tags,
        )
        self.session.add(new_post)
        await self.session.flush()
        post_vo.tags = [Tag(id=tag.id, name=tag.name) for tag in new_post.tags]
        return post_vo

    async def find_by_id(self, id: int) -> PostVO:
        async with self.session as session:
            query = await session.exec(
                select(Post).options(selectinload(Post.tags)).where(Post.id == id).select_from(Post)
            )
            post = query.one_or_none()
            if post:
                return PostVO(
                    id=post.id,
                    title=post.title,
                    contents=post.contents,
                    author_id=post.author_id,
                    tags=[Tag(id=tag.id, name=tag.name) for tag in post.tags],
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )

    async def find_all(
        self, limit: int, offset: int, tag_ids: list[int] = None, author_id: int = None
    ) -> tuple[int, list[PostVO]]:
        query = select(Post)
        total_count_query = await self.session.exec(select(func.count()).select_from(query.subquery()))
        total_count = total_count_query.one()

        query = query.options(selectinload(Post.tags))
        if tag_ids is not None:
            query = query.where(Post.tags.any(Tag.id.in_(tag_ids)))
        if author_id:
            query = query.where(Post.author_id == author_id)

        query = query.limit(limit).offset(offset)
        async with self.session as session:
            posts = await session.exec(query)
            return total_count, [
                PostVO(
                    id=post.id,
                    title=post.title,
                    contents=post.contents,
                    author_id=post.author_id,
                    tags=[Tag(id=tag.id, name=tag.name) for tag in post.tags],
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
                for post in posts.all()
            ]

    async def delete(self, post_id: int):
        query = select(Post).where(Post.id == post_id)
        query = await self.session.execute(query)
        post = query.scalar_one_or_none()
        if post:
            await self.session.delete(post)
            await self.session.flush()
