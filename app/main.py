import asyncio

from fastapi import FastAPI

from app.routes import router
from config.database import check_async_database_pool
from config.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup():
    asyncio.create_task(check_async_database_pool())
