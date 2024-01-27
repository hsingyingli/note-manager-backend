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
    db_driver: str = Field(alias="db_driver", default="postgresql")

    # timezone
    timezone: str = Field(alias="timezone", default="")


if __name__ == "__main__":
    print(Settings().model_dump())  # pyright: ignore
    print("===")
    print(Settings().test())
