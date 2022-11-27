from sanic_ext import Extend
from sanic import Sanic, Request
from sanic.response import json

from my_locations_api.locations import locations_blueprint


api: Sanic = Sanic("my-locations")

api.config.FALLBACK_ERROR_FORMAT = "json"
api.config.CORS_ORIGINS = "http://mylocations.local"

Extend(api)

api.blueprint(locations_blueprint)


@api.get("/")
async def hello_world(request: Request):
    return json({ "Hello": "world!" })
