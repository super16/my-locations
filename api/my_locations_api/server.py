from sanic import Sanic

from my_locations_api.database import DatabaseConnection
from my_locations_api.config import DatabaseConfig
from my_locations_api.utils import create_app


api: Sanic = create_app(
    "my_locations",
    DatabaseConfig,
    DatabaseConnection,
)
