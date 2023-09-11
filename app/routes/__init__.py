from fastapi import APIRouter
from app.routes.v1 import v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1", tags=["version 1"])
