from sqlmodel import Field, SQLModel, Relationship
from common.base_db_models import BaseSQLModel


class PostTagLink(SQLModel, table=True):
    post_id: str = Field(foreign_key="post.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=36)
    name: str = Field(unique=True, max_length=32)
    posts: list["Post"] = Relationship(back_populates="tags", link_model=PostTagLink)


class Post(BaseSQLModel, table=True):
    id: str = Field(primary_key=True, max_length=36)
    author_id: str = Field(foreign_key="user.id")
    title: str = Field(primary_key=True, max_length=128)
    contents: str = Field()
    tags: list[Tag] = Relationship(back_populates="posts", link_model=PostTagLink)
