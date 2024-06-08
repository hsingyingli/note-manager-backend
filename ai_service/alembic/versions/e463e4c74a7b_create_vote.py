"""create_vote

Revision ID: e463e4c74a7b
Revises: 0e00b49d1fd3
Create Date: 2024-04-14 17:02:34.464426

"""
from typing import Sequence, Union

from sqlalchemy.sql import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e463e4c74a7b"
down_revision: Union[str, None] = "0e00b49d1fd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
                CREATE TYPE "vote_type" AS ENUM (
                'UP',
                'DOWN'
                );

                CREATE TABLE "votes" (
                "id" bigserial PRIMARY KEY,
                "user_id" int8,
                "note_id" int8,
                "type" vote_type NOT NULL,
                "created_at" timestamptz DEFAULT (now()),
                "updated_at" timestamptz DEFAULT (now())
                );

                CREATE INDEX ON "votes" ("user_id", "note_id");
                ALTER TABLE "votes" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
                ALTER TABLE "votes" ADD FOREIGN KEY ("note_id") REFERENCES "notes" ("id");
            """
        ),
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            DROP TABLE IF EXISTS votes;
            DROP TYPE IF EXISTS vote_type;
        """
        )
    )
