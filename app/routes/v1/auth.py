from typing import Annotated, Union

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import Response
from psycopg_pool.pool_async import AsyncConnectionPool

from app.repositories.session_repository.query import (GetSessionByIdParam,
                                                       get_session_by_id)
from app.services.security.token import create_token, verify_token
from config.database import get_async_database_pool
from config.setting import get_settings

settings = get_settings()
auth_router = APIRouter()


@auth_router.post("/renew_access")
async def renew_access_token(
    note_app_refresh_token: Annotated[Union[str, None], Cookie()] = None,
    db_pool: AsyncConnectionPool = Depends(get_async_database_pool),
):
    if note_app_refresh_token is None:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    payload = verify_token(note_app_refresh_token)
    if payload.is_failed:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            session = await get_session_by_id(
                cur, GetSessionByIdParam(id=payload.result.id)
            )
    if session.is_failed or session.result.refresh_token != note_app_refresh_token:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    access_token, _ = create_token(payload.result.email, settings.access_token_duration)

    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.set_cookie(key="note_app_access_token", value=access_token)
    return response
