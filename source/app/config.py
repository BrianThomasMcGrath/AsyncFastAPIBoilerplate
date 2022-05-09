from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    db_host: str
    db_port: str = 5432
    db_username: str
    db_password: str
    db_name: str = "tweetboard"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Config:
    return Config()
