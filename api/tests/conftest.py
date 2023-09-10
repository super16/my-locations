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
def testing_config() -> ApplicationConfig | type[ApplicationConfig]:
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
def standalone_single_location() -> tuple[str, dict[str, float | str]]:
    return (
        (
            "/v1/locations?"
            "end_latitude=85.0&end_longitude=46.0&"
            "start_latitude=65.0&start_longitude=30.0"
        ),
        {
            "title": "Standalone single location",
            "description": "Standalone single location description",
            "latitude": 75.0,
            "longitude": 35.0,
        },
    )


@fixture(scope="session")
def new_location() -> dict[str, float | str]:
    return {
        "title": "New location",
        "description": "New location description",
        "latitude": 55.0,
        "longitude": 15.0,
    }


@fixture(scope="session")
def get_locations_path() -> str:
    return (
        "/v1/locations?"
        "end_latitude=62.0&end_longitude=26.0&"
        "start_latitude=52.0&start_longitude=9.0"
    )


@fixture(scope="session")
def update_for_location() -> dict[str, str]:
    return {
        "title": "Updated title",
        "description": "Updated description",
    }
