from dataclasses import dataclass, fields

from sanic.exceptions import BadRequest


@dataclass
class LocationItemBase:
    title: str
    description: str

    def __post_init__(self) -> None:
        """Validate fields for empty values"""
        invalid_fields: list[str] = [
            field.name for field in fields(self)
            if not getattr(self, field.name)
        ]
        if invalid_fields:
            error_message: str = "Input should not be empty"
            raise BadRequest(
                error_message,
                context={"invalid_fields": invalid_fields},
            )


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
