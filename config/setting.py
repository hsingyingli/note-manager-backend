from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # db settings
    db_port: int = Field(alias="db_port", default="3306")
    db_name: str = Field(alias="db_name", default="")
    db_user: str = Field(alias="db_user", default="")
    db_password: str = Field(alias="db_password", default="")
    db_host: str = Field(alias="db_host", default="")

    # timezone
    timezone: str = Field(alias="timezone", default="")

    # jwt
    symmetric_key: str = Field(alias="symmetric_key")


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()


if __name__ == "__main__":
    print(Settings().model_dump())  # pyright: ignore
    print("===")
    print(Settings().test())
