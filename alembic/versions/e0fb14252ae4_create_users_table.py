"""create user table

Revision ID: e0fb14252ae4
Revises: 
Create Date: 2024-01-27 15:28:28.966628

"""
from typing import Sequence, Union

from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e0fb14252ae4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE "users" (
            "id" bigserial PRIMARY KEY,
            "username" varchar(32) UNIQUE NOT NULL,
            "email" varchar(32) UNIQUE NOT NULL,
            "password" varchar(256) NOT NULL,
            "created_at" timestamptz NOT NULL DEFAULT (now()),
            "updated_at" timestamptz NOT NULL DEFAULT (now())
            );
            """
        ),
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
        DROP TABLE IF EXISTS users;
        """
        )
    )
