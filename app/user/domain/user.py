from datetime import datetime
from dataclasses import dataclass


@dataclass
class Profile:

    name: str
    age: int | None
    phone: str | None


@dataclass
class User:
    id: str
    email: str
    profile: Profile
    password: str
    created_at: datetime
    updated_at: datetime
