from dataclasses import dataclass, fields
from typing import List


@dataclass
class LocationItemBase:
    title: str
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


def invalid_location_item_fields(data_class: LocationItemBase) -> List[str]:
    """
    Validate fields of Location dataclasses for empty values.

    Args:
        data_class: Input dataclass entity.

    Returns:
        List of string with names of invalid fields.
    """
    return [
        field.name for field in fields(data_class)
        if not getattr(data_class, field.name)
    ]
