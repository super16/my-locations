from dataclasses import dataclass


@dataclass
class LocationItemBase:
    description: str


@dataclass
class LocationItem(LocationItemBase):
    latitude: float
    longitude: float


@dataclass
class MapBounds:
    end_latitude: float
    end_longitude: float
    start_latitude: float
    start_longitude: float
