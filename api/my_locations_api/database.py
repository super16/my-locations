from sanic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseConnection:

    """Connection class to PostgreSQL database."""

    def __init__(self, config: Config) -> None:
        self._url: str = "".join([
            f"{config.DB_ENGINE}://",
            f"{config.DB_USER}:{config.DB_PASSWORD}@",
            f"{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        ])
        self._connection: AsyncEngine = create_async_engine(self._url)
        self._session_factory: async_sessionmaker[AsyncSession] = \
            async_sessionmaker(
                self._connection, expire_on_commit=False,
            )

    @property
    def create_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
