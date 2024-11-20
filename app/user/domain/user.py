from datetime import datetime
from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    age: int
    phone: str


@dataclass
class User:
    id: str
    email: str
    profile: Profile | None
    password: str
    created_at: datetime
    updated_at: datetime
