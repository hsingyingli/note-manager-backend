"""create_note

Revision ID: 0e00b49d1fd3
Revises: 9e7c87b0663a
Create Date: 2024-04-14 16:22:16.332916

"""
from typing import Sequence, Union

from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0e00b49d1fd3"
down_revision: Union[str, None] = "9e7c87b0663a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TABLE "notes" (
                "id" bigserial PRIMARY KEY,
                "uuid" uuid NOT NULL DEFAULT (uuid_generate_v1()),
                "user_id" int8,
                "title" varchar NOT NULL,
                "content" json DEFAULT '{}'::JSON,
                "published_at" timestamptz DEFAULT null,
                "created_at" timestamptz DEFAULT (now()),
                "updated_at" timestamptz DEFAULT (now())
                );
                CREATE INDEX ON "notes" ("uuid");
                ALTER TABLE "notes" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;
            """
        ),
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            DROP TABLE IF EXISTS notes;
        """
        )
    )
