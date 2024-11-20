from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_username: str
    database_password: str
    database_name: str
    database_url: str
    jwt_secret: str
    celery_broker_url: str
    celery_backend_url: str

    @property
    def sqlalchemy_database_url(self):
        return f"mysql+aiomysqldb://{self.database_username}:{self.database_password}@{self.database_url}/{self.database_name}"


@lru_cache
def get_settings():
    return Settings()
