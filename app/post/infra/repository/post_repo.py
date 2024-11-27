from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.post.domain.post import Post as PostVO
from app.post.infra.model.post import Tag, Post
from app.post.domain.repository.post_repo import AbcPostRepository
from core.database import session


class PostRepository(AbcPostRepository):
    async def delete_tags(self, user_id: str, id: str):
        post_query = await session.execute(
            select(Post).where(Post.author_id == user_id, Post.id == id).options(selectinload(Post.tags))
        )
        post = post_query.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=422)
        post.tags = []
        session.add(post)
        await session.commit()

        unused_tags_query = await session.execute(select(Tag).where(~Tag.posts.any()))
        unused_tags = unused_tags_query.scalars().all()
        for tag in unused_tags:
            await session.delete(tag)
        await session.commit()

    async def update(self, id: str, post_vo: PostVO) -> PostVO:
        await self.delete_tags(user_id=post_vo.author_id, id=id)
        query = await session.execute(select(Post).options(selectinload(Post.tags)).where(Post.id == id))
        post = query.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=422)
        post.title = post_vo.title
        post.contents = post_vo.contents
        tag_names = [tag.name for tag in post_vo.tags]
        tags_query = await session.execute(select(Tag).where(Tag.name.in_(tag_names)))
        saved_tags: list[Tag] = tags_query.scalars().all()
        tags: list[Tag] = []
        saved_tags_dict = {tag.name: tag for tag in saved_tags}
        for tag in post_vo.tags:
            if tag.name in saved_tags_dict:
                tags.append(saved_tags_dict[tag.name])
            else:
                tags.append(Tag(id=tag.id, name=tag.name))
        post.tags = tags
        session.add(post)
        await session.flush()
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
        tags_query = await session.execute(select(Tag).where(Tag.name.in_(tag_names)))
        saved_tags: list[Tag] = tags_query.scalars().all()
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
        session.add(new_post)
        await session.flush()
        post_vo.tags = [Tag(id=tag.id, name=tag.name) for tag in new_post.tags]
        return post_vo

    async def find_by_id(self, id: int) -> PostVO:
        query = await session.execute(select(Post).options(selectinload(Post.tags)).where(Post.id == id))
        post = query.scalar_one_or_none()
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

        total_count_query = await session.execute(select(func.count()).select_from(query.subquery()))
        total_count = total_count_query.scalar_one()

        query = query.options(selectinload(Post.tags))
        if tag_ids is not None:
            query = query.where(Post.tags.any(Tag.id.in_(tag_ids)))
        if author_id:
            query = query.where(Post.author_id == author_id)

        query = query.limit(limit).offset(offset)
        posts = await session.execute(query)
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
            for post in posts.scalars()
        ]

    async def delete(self, post_id: int):
        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query).scalar_one_or_none()
        if post:
            session.delete(post)
            await session.flush()
