from datetime import datetime

from psycopg import AsyncCursor
from pydantic import UUID4, BaseModel

from app.models.session import Session
from app.repositories.session_repository.sql import (create_session_query,
                                                     expire_session_query,
                                                     get_session_by_id_query)
from app.utils.monadic import async_monadic
from config.timezone import get_timezone

timezone = get_timezone()


class CreateSessionParam(BaseModel):
    id: UUID4
    user_id: int
    expired_at: datetime
    refresh_token: str


@async_monadic
async def create_session(cursor: AsyncCursor, param: CreateSessionParam) -> Session:
    await cursor.execute(
        create_session_query,
        list(param.model_dump().values()),
    )
    result = await cursor.fetchone()
    if result is None:
        raise Exception("Create Session Failed")
    return Session(id=result[0])


class GetSessionByIdParam(BaseModel):
    id: str
    expired_at: datetime = datetime.now(timezone)


@async_monadic
async def get_session_by_id(cursor: AsyncCursor, param: GetSessionByIdParam) -> Session:
    await cursor.execute(
        get_session_by_id_query,
        list(param.model_dump().values()),
    )
    result = cursor.fetchone()
    if result is None:
        raise Exception("Session found")

    return Session(id=result[0], user_id=result[1], refresh_token=result[2])


class ExpireSessionParam(BaseModel):
    expired_at: datetime = datetime.now(timezone)
    id: str


@async_monadic
async def expire_session(cursor: AsyncCursor, param: ExpireSessionParam):
    await cursor.execute(
        expire_session_query,
        list(param.model_dump().values()),
    )
