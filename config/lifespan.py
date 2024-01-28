from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import get_async_database_pool


# configure life span
@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start
    pool = get_async_database_pool()
    await pool.wait()
    yield
    # after app end
    await pool.close()
