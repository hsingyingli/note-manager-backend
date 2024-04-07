"""user table add index on email

Revision ID: 2b08a718e445
Revises: e0fb14252ae4
Create Date: 2024-01-28 14:57:30.483353

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2b08a718e445"
down_revision: Union[str, None] = "e0fb14252ae4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            CREATE INDEX index_users_on_email ON users (email);
            """
        ),
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            DROP INDEX IF EXISTS index_users_on_email
            """
        ),
    )
