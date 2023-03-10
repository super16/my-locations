from typing import Any

from sanic import Sanic

from my_locations_api.database import DatabaseConnection
from my_locations_api.blueprints import locations_blueprint


def create_app(
    title: str,
    config: Any,
    conn: DatabaseConnection,
) -> Sanic:

    app = Sanic(title)
    app.update_config(config())

    app.config.FALLBACK_ERROR_FORMAT = "json"
    app.config.CORS = False

    @app.before_server_start
    async def setup_db(application: Sanic, _) -> None:
        db_conn = conn(application.config)
        app.ext.dependency(db_conn)

    app.blueprint(locations_blueprint)

    return app
