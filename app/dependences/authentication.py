from typing import Annotated, Union

from fastapi import Cookie, Depends, HTTPException, status
from psycopg_pool.pool_async import AsyncConnectionPool

from app.models.user import User
from app.repositories.user_repository.query import (GetUserByEmailParam,
                                                    get_user_by_email)
from app.services.security.token import verify_token
from config.database import get_async_database_pool


async def get_user_from_token(
    note_app_access_token: Annotated[Union[str, None], Cookie()] = None,
    db_pool: AsyncConnectionPool = Depends(get_async_database_pool),
) -> User:
    if note_app_access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    payload = verify_token(note_app_access_token)
    if payload.is_failed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            user = await get_user_by_email(
                cur, GetUserByEmailParam(email=payload.result.email)
            )
    if user.is_failed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return user.result
