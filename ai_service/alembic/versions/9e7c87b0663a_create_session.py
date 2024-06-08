"""create_session

Revision ID: 9e7c87b0663a
Revises: 2b08a718e445
Create Date: 2024-04-06 16:37:04.858716

"""
from typing import Sequence, Union

from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9e7c87b0663a"
down_revision: Union[str, None] = "2b08a718e445"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE TABLE "sessions" (
            "id" uuid NOT NULL,
            "user_id" int8 NOT NULL,
            "expired_at" timestamptz NOT NULL DEFAULT (now()),
            "created_at" timestamptz NOT NULL DEFAULT (now()),
            "updated_at" timestamptz NOT NULL DEFAULT (now()),
            "refresh_token" varchar(256) NOT NULL,
            PRIMARY KEY (id),
            CONSTRAINT fk_user
                FOREIGN KEY(user_id) 
                    REFERENCES users(id)
            );
            """
        ),
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
        DROP TABLE IF EXISTS sessions;
        """
        )
    )
