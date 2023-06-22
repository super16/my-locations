from typing import Type

from sanic import Sanic

from my_locations_api.blueprints import locations_blueprint
from my_locations_api.config import ApplicationConfig
from my_locations_api.database import DatabaseConnection


def create_app(title: str, config: Type[ApplicationConfig]) -> Sanic:

    app = Sanic(title)
    app.update_config(config)

    app.config.AUTO_RELOAD = config.DEBUG
    app.config.cors = False
    app.config.FALLBACK_ERROR_FORMAT = "json"

    @app.before_server_start
    async def setup_db(application: Sanic, _) -> None:
        db_conn: DatabaseConnection = DatabaseConnection(application.config)
        app.ext.dependency(db_conn.create_session())

    app.blueprint(locations_blueprint)

    return app
