from typing import Annotated, Union

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse, Response
from psycopg.errors import UniqueViolation
from psycopg_pool.pool_async import AsyncConnectionPool
from pydantic import BaseModel, EmailStr, Field

from app.dependences.authentication import get_user_from_token
from app.models.user import User
from app.repositories.session_repository.query import (CreateSessionParam,
                                                       ExpireSessionParam,
                                                       create_session,
                                                       expire_session)
from app.repositories.user_repository.query import (CreateUserParam,
                                                    GetUserByEmailParam,
                                                    create_user,
                                                    get_user_by_email)
from app.services.security.password import check_password, hash_password
from app.services.security.token import create_token, verify_token
from config.database import get_async_database_pool
from config.setting import get_settings

settings = get_settings()
user_router = APIRouter()


@user_router.get("/")
def get_user_route(user: User = Depends(get_user_from_token)):
    return {"user": user}


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_route(
    param: CreateUserParam,
    db_pool: AsyncConnectionPool = Depends(get_async_database_pool),
):
    param.password = hash_password(param.password)
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            result = await create_user(cur, param)

    if result.is_failed:
        msg = (
            "Email or Password Has Been Taken."
            if type(result.errors) == UniqueViolation
            else "Try Later."
        )

        status_code = (
            status.HTTP_400_BAD_REQUEST
            if type(result.errors) == UniqueViolation
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return JSONResponse(content={"msg": msg}, status_code=status_code)


class LoginUserParam(BaseModel):
    email: EmailStr
    password: str = Field(pattern=r"^[0-9a-zA-Z]{8,12}$")


@user_router.post("/login")
async def login_user_route(
    param: LoginUserParam,
    db_pool: AsyncConnectionPool = Depends(get_async_database_pool),
):
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            user = await get_user_by_email(cur, GetUserByEmailParam(email=param.email))
    if user.is_failed:
        return JSONResponse(
            content={"msg": "Not Found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    verified = check_password(param.password, user.result.password)

    if not verified:
        return JSONResponse(
            content={"msg": "Invalid Password"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    # create token
    access_token, access_payload = create_token(
        param.email, settings.access_token_duration
    )
    refresh_token, refresh_payload = create_token(
        param.email, settings.refresh_token_duration
    )

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            session = await create_session(
                cur,
                CreateSessionParam(
                    id=refresh_payload.id,
                    user_id=user.result.id,
                    expired_at=refresh_payload.exp,
                    refresh_token=refresh_token,
                ),
            )
    if session.is_failed:
        return JSONResponse(
            content={"msg": "Try Later"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    response = JSONResponse(
        content={"msg": "succeeded"}, status_code=status.HTTP_200_OK
    )
    response.set_cookie(
        key="note_app_access_token",
        value=access_token,
        domain="127.0.0.1",
        max_age=settings.access_token_duration,
    )
    response.set_cookie(
        key="note_app_refresh_token",
        value=refresh_token,
        domain="127.0.0.1",
        max_age=settings.refresh_token_duration,
    )

    return response


@user_router.post("/logout")
async def logout_user(
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
            result = await expire_session(cur, ExpireSessionParam(id=payload.result.id))

    if result.is_failed:
        return JSONResponse(
            content={"msg": "Try Later"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.set_cookie(
        key="note_app_access_token", value="", max_age=-1, domain="127.0.0.1"
    )
    response.set_cookie(
        key="note_app_refresh_token", value="", max_age=-1, domain="127.0.0.1"
    )
    return response
