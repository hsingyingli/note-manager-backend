from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from psycopg_pool.pool_async import AsyncConnectionPool
from returns.io import IOFailure

from app.repositories.UserRepository import UserRepository
from app.utils.password import hash_password
from config.database import get_async_database_pool

user_router = APIRouter()

from pydantic import BaseModel, EmailStr, Field


@user_router.get("/")
def get_user():
    return {}


class UserInfo(BaseModel):
    username: str = Field(pattern=r"^[0-9a-zA-Z]{6,18}$")
    email: EmailStr
    password: str = Field(pattern=r"^[0-9a-zA-Z]{8,12}$")


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_info: UserInfo, db_pool: AsyncConnectionPool = Depends(get_async_database_pool)
):
    user_info.password = hash_password(user_info.password)
    result = await UserRepository.create(db_pool, **user_info.model_dump())
    if isinstance(result, IOFailure):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "username, email or password has been taken"},
        )


@user_router.post("/login")
def login_user():
    return {}


@user_router.post("/logout")
def logout_user():
    return {}
