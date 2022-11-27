from sqlalchemy import (
    DECIMAL,
    INTEGER,
    TEXT,
    VARCHAR,
    Column,
    DateTime,
    text,
)

from alembic import op

revision = "0ab771887834"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "location",
        Column(
            "location_id",
            INTEGER,
            autoincrement=True,
            index=True,
            primary_key=True,
            unique=True,
        ),
        Column("title", VARCHAR(64), nullable=False),
        Column("description", TEXT(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            server_default=text("now()"),
            nullable=True,
        ),
        Column(
            "updated_at",
            DateTime(),
            server_default=text("now()"),
            nullable=True,
        ),
        Column("latitude", DECIMAL(8, 6), nullable=False),
        Column("longitude", DECIMAL(8, 6), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("locations")
