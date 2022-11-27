from contextvars import ContextVar
from os import getenv

from sanic import Request, Sanic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from my_locations_api.blueprints import locations_blueprint

# Application and its config

api: Sanic = Sanic("my_locations")

api.config.FALLBACK_ERROR_FORMAT = "json"
api.config.CORS = False


# Initialize database connection

_base_model_session_ctx: ContextVar = ContextVar("session")


@api.before_server_start
async def setup_db(api: Sanic, _) -> None:

    engine = "postgresql+asyncpg"
    user = getenv('POSTGRES_USER', 'user')
    password = getenv('POSTGRES_PASSWORD', 'password')
    host = getenv('GATEWAY_ADDRESS', '172.28.5.254')
    port = getenv('POSTGRES_PORT', '5432')
    name = getenv('POSTGRES_DB', 'locations')

    api.ctx.bind = create_async_engine(
        f"{engine}://{user}:{password}@{host}:{port}/{name}",
    )


@api.on_request
async def inject_session(request: Request) -> None:
    _sessionmaker: sessionmaker[Session] = sessionmaker(
        api.ctx.bind, class_=AsyncSession, expire_on_commit=False,
    )
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = \
        _base_model_session_ctx.set(request.ctx.session)


@api.on_response
async def close_session(request: Request, response) -> None:
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


# Add blueprints to application

api.blueprint(locations_blueprint)
