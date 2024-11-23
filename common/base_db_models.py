from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


def get_utc_now():
    return datetime.now(timezone.utc)


class BaseSQLModel(SQLModel):
    created_at: datetime = Field(default=get_utc_now())
    updated_at: datetime = Field(default=get_utc_now())
