import asyncio
from functools import lru_cache

from psycopg_pool import AsyncConnectionPool

from config.setting import get_settings

settings = get_settings()

DATABASE_DSN = f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
CONNECTION_INFO = f"dbname={settings.db_name} user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port}"


@lru_cache
def get_async_database_pool():
    return AsyncConnectionPool(CONNECTION_INFO)


async def check_async_database_pool() -> None:
    print("Start checking database")
    pool = get_async_database_pool()
    while True:
        await asyncio.sleep(500)
        pool.check()
