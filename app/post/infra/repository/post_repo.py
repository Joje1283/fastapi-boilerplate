from sqlmodel import select

from app.post.domain.post import Post as PostVO
from app.post.infra.model.post import Tag, Post
from app.post.domain.repository.post_repo import AbcPostRepository
from core.database import session


class PostRepository(AbcPostRepository):
    async def save(self, post_vo: PostVO) -> PostVO:
        # Upsert tags
        tag_ids = [tag.id for tag in post_vo.tags]
        tags_query = await session.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        saved_tags: list[Tag] = tags_query.all()
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
        pass

    async def find_all(
        self, limit: int, offset: int, tag_ids: list[int], author_id: int = None
    ) -> tuple[int, list[PostVO]]:
        pass

    async def delete(self, post_id: int):
        pass
