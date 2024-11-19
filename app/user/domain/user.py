from datetime import datetime
from dataclasses import dataclass


@dataclass
class Profile:
    email: str
    name: str
    age: int | None
    phone: str | None


@dataclass
class User:
    id: str
    profile: Profile
    created_at: datetime
    updated_at: datetime
