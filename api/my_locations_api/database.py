from sanic.config import Config
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from my_locations_api.config import ApplicationConfig


class DatabaseConnection:

    """Connection to database wrapper."""

    def __init__(self, config: Config | ApplicationConfig) -> None:
        self._url: URL = URL.create(
            config.DB_ENGINE,
            config.DB_USER,
            config.DB_PASSWORD,
            config.DB_HOST,
            config.DB_PORT,
            config.DB_NAME,
        )
        self._connection: AsyncEngine = create_async_engine(
            self._url, echo=config.DEBUG,
        )
        self._session_factory: async_sessionmaker[AsyncSession] = \
            async_sessionmaker(
                self._connection, expire_on_commit=False,
            )

    def create_session(self) -> AsyncSession:
        return self._session_factory()
