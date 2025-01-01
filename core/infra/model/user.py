from sqlmodel import Field

from core.infra.base_db_models import BaseSQLModel


class User(BaseSQLModel, table=True):
    id: str = Field(primary_key=True, max_length=36)
    email: str = Field(max_length=64, unique=True)
    password: str = Field(max_length=64)


class Profile(BaseSQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: str = Field(foreign_key="user.id")
    name: str = Field(max_length=32)
    age: int = Field()
    phone: str = Field(max_length=16)
