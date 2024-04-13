from psycopg import AsyncCursor
from pydantic import BaseModel, EmailStr, Field

from app.models.user import User
from app.repositories.user_repository.sql import (create_user_query,
                                                  get_user_by_email_query)
from app.utils.monadic import async_monadic


class CreateUserParam(BaseModel):
    username: str = Field(pattern=r"^[0-9a-zA-Z]{6,18}$")
    email: EmailStr
    password: str = Field(pattern=r"^[0-9a-zA-Z]{8,12}$")


@async_monadic
async def create_user(cursor: AsyncCursor, param: CreateUserParam):
    await cursor.execute(
        create_user_query,
        list(param.model_dump().values()),
    )


class GetUserByEmailParam(BaseModel):
    email: str


@async_monadic
async def get_user_by_email(cursor: AsyncCursor, param: GetUserByEmailParam) -> User:
    await cursor.execute(
        get_user_by_email_query,
        list(param.model_dump().values()),
    )
    result = await cursor.fetchone()
    if result is None:
        raise Exception("not found")
    return User(id=result[0], username=result[1], email=result[2], password=result[3])
