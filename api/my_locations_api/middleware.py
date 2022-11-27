from contextvars import ContextVar

from sanic import Request, Sanic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


api: Sanic = Sanic.get_app()

_base_model_session_ctx: ContextVar = ContextVar("session")


@api.on_request
async def inject_session(request: Request) -> None:
    request.ctx.session = sessionmaker(
        api.ctx.bind,
        AsyncSession,
        expire_on_commit=False
    )()
    request.ctx.session_ctx_token = \
        _base_model_session_ctx.set(request.ctx.session)


@api.on_response
async def close_session(request: Request, response) -> None:
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
