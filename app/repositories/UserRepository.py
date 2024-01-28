from psycopg_pool.pool_async import AsyncConnectionPool
from returns.future import future_safe


class UserRepository:
    @classmethod
    @future_safe
    async def create(
        cls,
        db_pool: AsyncConnectionPool,
        username: str,
        email: str,
        password: str,
    ):
        async with db_pool.connection() as conn:
            await conn.execute(
                """
                INSERT INTO users (
                    username, email, password
                ) VALUES (
                    %s, %s, %s
                ) RETURNING *;
                """,
                (username, email, password),
            )
