from sqlalchemy import (
    DECIMAL,
    INTEGER,
    TEXT,
    VARCHAR,
    Column,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp

from alembic.op import create_table, drop_table


revision = "0ab771887834"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    create_table(
        "location",
        Column("location_id", INTEGER(), primary_key=True),
        Column("title", VARCHAR(64), nullable=False),
        Column("description", TEXT(), nullable=False),
        Column("latitude", DECIMAL(8, 6), nullable=False),
        Column("longitude", DECIMAL(8, 6), nullable=False),
        Column(
            "created_at",
            TIMESTAMP(),
            server_default=current_timestamp(),
            nullable=False,
        ),
        Column(
            "updated_at",
            TIMESTAMP(),
            onupdate=current_timestamp(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    drop_table("location")
