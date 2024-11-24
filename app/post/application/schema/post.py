from pydantic import BaseModel


class PostCommand(BaseModel):
    title: str
    content: str
    author_id: str
    tags: list[str]


class PostsQuery(BaseModel):
    author_id: str | None
    tag: list[int]
    limit: int
    offset: int
