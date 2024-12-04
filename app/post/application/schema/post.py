from pydantic import BaseModel


class PostCommand(BaseModel):
    title: str | None
    contents: str | None
    author_id: str | None
    tags: list[str] | None


class PostsQuery(BaseModel):
    author_id: str | None
    tags: list[int] | None
    limit: int
    offset: int
