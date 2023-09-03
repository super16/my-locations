from os import getenv

from sanic.config import Config


class ApplicationConfig(Config):
    DB_ENGINE: str = "postgresql+asyncpg"
    DB_USER: str = getenv("POSTGRES_USER", "user")
    DB_PASSWORD: str = getenv("POSTGRES_PASSWORD", "password")
    DB_HOST: str = "locations_db"
    DB_PORT: int = int(getenv("POSTGRES_PORT", 5432))
    DB_NAME: str = getenv("POSTGRES_DB", "locations")

    DEBUG: bool = bool(getenv("DEBUG", False))
