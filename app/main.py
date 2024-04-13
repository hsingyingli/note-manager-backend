import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from config.database import check_async_database_pool
from config.lifespan import lifespan

app = FastAPI(lifespan=lifespan)


origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup():
    asyncio.create_task(check_async_database_pool())
