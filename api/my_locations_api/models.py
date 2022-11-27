from sqlalchemy import Column, INTEGER, NUMERIC, TEXT

from database import Base


class Location(Base):

    __tablename__ = "locations"
    id = Column(
        INTEGER(),
        autoincrement=True,
        index=True,
        primary_key=True,
        unique=True
    )
    latitude = Column(NUMERIC(), nullable=False)
    longitude = Column(NUMERIC(), nullable=False)
    description = Column(TEXT(), nullable=False)
