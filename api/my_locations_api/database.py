from typing import Any

from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData


api: Sanic = Sanic.get_app()

Base: Any = declarative_base()

base_metadata: MetaData = Base.metadata


@api.before_server_start
async def create_db_engine(api: Sanic, _) -> None:
    api.ctx.bind: AsyncEngine = create_async_engine(
        "postgresql+asyncpg://user:password@172.161.13.12:5432/locations"
    )
    connection: AsyncConnection
    async with api.ctx.bind.begin() as connection:
        await connection.run_sync(base_metadata.create_all)
