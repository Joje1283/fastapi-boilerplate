from dataclasses import dataclass


@dataclass
class Tag:
    id: int
    name: str


@dataclass
class Post:
    id: int
    title: str
    content: str
    author_id: int
    tags: list[Tag]
    created_at: str
    updated_at: str
