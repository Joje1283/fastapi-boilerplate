from pydantic import BaseModel


class PostCommand(BaseModel):
    title: str
    contents: str
    author_id: str
    tags: list[str]


class PostsQuery(BaseModel):
    author_id: str | None
    tags: list[int] | None
    limit: int
    offset: int
