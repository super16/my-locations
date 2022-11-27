from datetime import datetime
from typing import Any

from sqlalchemy import (
    DECIMAL,
    INTEGER,
    TEXT,
    VARCHAR,
    Column,
    DateTime,
    text,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

Base: Any = declarative_base()

base_metadata: MetaData = Base.metadata


class Location(Base):

    __tablename__ = "location"

    location_id = Column(
        INTEGER(),
        autoincrement=True,
        index=True,
        primary_key=True,
        unique=True,
    )
    title = Column(VARCHAR(64), nullable=False)
    description = Column(TEXT(), nullable=False)
    created_at = Column(
        DateTime(),
        default=datetime.utcnow,
        server_default=text('now()'),
    )
    updated_at = Column(
        DateTime(),
        default=datetime.utcnow,
        server_default=text('now()'),
    )
    latitude: Column[float] = Column(DECIMAL(8, 6), nullable=False)
    longitude: Column[float] = Column(DECIMAL(9, 6), nullable=False)

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
