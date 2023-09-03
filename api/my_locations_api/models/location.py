from datetime import datetime

from sqlalchemy import DECIMAL, INTEGER, TEXT, VARCHAR
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.sql.functions import current_timestamp


class Base(DeclarativeBase):
    pass


class Location(Base):

    __tablename__ = "location"

    location_id: Mapped[int] = mapped_column(INTEGER(), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(8, 6), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        server_default=current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        onupdate=current_timestamp(),
    )

    def serialize(self) -> dict:
        """Serialize Location object to Python dictionary.

        Returns:
            Location object as dictionary.
        """
        return {
            "id": self.location_id,
            "title": self.title,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
