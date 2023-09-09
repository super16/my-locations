from asyncio import run
from logging.config import fileConfig
from os import getenv

from sqlalchemy import URL
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.pool import NullPool

from alembic.context import (
    begin_transaction,
    config,
    configure,
    is_offline_mode,
    run_migrations,
)


alembic_config = config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = None

url = URL.create(
    drivername="postgresql+asyncpg",
    username=getenv("POSTGRES_USER", "user"),
    password=getenv("POSTGRES_PASSWORD", "password"),
    host="locations_db",
    database=getenv("POSTGRES_DB", "locations"),
)

config.set_main_option(
    "sqlalchemy.url", url.render_as_string(hide_password=False),
)


def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with begin_transaction():
        run_migrations()


def do_run_migrations(connection: Connection) -> None:
    configure(connection=connection, target_metadata=target_metadata)

    with begin_transaction():
        run_migrations()


async def run_async_migrations() -> None:
    config_ini_section = alembic_config.get_section(
        alembic_config.config_ini_section,
    )

    if config_ini_section:
        connectable = async_engine_from_config(
            config_ini_section,
            prefix="sqlalchemy.",
            poolclass=NullPool,
        )

        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

        await connectable.dispose()


def run_migrations_online() -> None:
    connectable = alembic_config.attributes.get("connection", None)
    if connectable is None:
        run(run_async_migrations())
    else:
        do_run_migrations(connectable)


if is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
