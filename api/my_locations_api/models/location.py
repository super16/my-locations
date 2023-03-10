from datetime import datetime

from sqlalchemy import (
    DECIMAL,
    INTEGER,
    TEXT,
    VARCHAR,
    DateTime,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Location(Base):

    __tablename__ = "location"

    location_id: Mapped[int] = mapped_column(
        INTEGER(),
        autoincrement=True,
        index=True,
        primary_key=True,
        unique=True,
    )
    title: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.utcnow,
        server_default=text('now()'),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.utcnow,
        server_default=text('now()'),
    )
    latitude: Mapped[float] = mapped_column(DECIMAL(8, 6), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6), nullable=False)

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
