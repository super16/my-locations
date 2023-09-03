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
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
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


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if is_offline_mode():
    run_migrations_offline()
else:
    run(run_migrations_online())
