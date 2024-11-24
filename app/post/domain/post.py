from datetime import datetime
from dataclasses import dataclass


@dataclass
class Tag:
    id: str
    name: str


@dataclass
class Post:
    id: str
    title: str
    content: str
    author_id: int
    tags: list[Tag]
    created_at: datetime
    updated_at: datetime
