from fastapi import APIRouter

from app.routes.v1.auth import auth_router
from app.routes.v1.user import user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
