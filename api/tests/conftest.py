from asyncio import AbstractEventLoop, get_event_loop_policy
from typing import AsyncGenerator, Generator

from pytest_asyncio import fixture
from sanic import Sanic
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from alembic.command import downgrade, upgrade
from alembic.config import Config
from my_locations_api.config import ApplicationConfig
from my_locations_api.utils import create_app


@fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
def testing_config() -> ApplicationConfig:
    application_config = ApplicationConfig
    application_config.DB_ENGINE = "postgresql+asyncpg"
    application_config.DB_USER = "test_user"
    application_config.DB_PASSWORD = "test_password"  # noqa: S105
    application_config.DB_HOST = "localhost"
    application_config.DB_NAME = "test_locations"
    application_config.DEBUG = True

    return application_config


@fixture(scope="session")
async def app(
    testing_config: ApplicationConfig,
) -> AsyncGenerator[Sanic, None]:
    database_uri = URL.create(
        drivername=testing_config.DB_ENGINE,
        username=testing_config.DB_USER,
        password=testing_config.DB_PASSWORD,
        host=testing_config.DB_HOST,
        port=testing_config.DB_PORT,
        database=testing_config.DB_NAME,
    )

    test_engine = create_async_engine(database_uri)

    def run_upgrade(connection, alembic_config: Config):
        alembic_config.attributes["connection"] = connection
        upgrade(alembic_config, "head")

    def run_downgrade(connection, alembic_config: Config):
        alembic_config.attributes["connection"] = connection
        downgrade(alembic_config, "base")

    async with test_engine.begin():
        test_alembic_config = Config("alembic.ini")
        test_alembic_config.set_main_option(
            "sqlalchemy.url",
            database_uri.render_as_string(hide_password=False),
        )
        async with test_engine.begin() as conn:
            await conn.run_sync(run_upgrade, test_alembic_config)

    yield create_app("testing_my_locations", testing_config)

    async with test_engine.begin() as conn:
        test_alembic_config = Config("alembic.ini")
        test_alembic_config.set_main_option(
            "sqlalchemy.url",
            database_uri.render_as_string(hide_password=False),
        )
        await conn.run_sync(run_downgrade, test_alembic_config)


@fixture(scope="session")
def map_bounds() -> dict[str, float]:
    return {
        "end_latitude": 2.9,
        "end_longitude": 2.9,
        "start_latitude": 2.2,
        "start_longitude": 2.2,
    }
