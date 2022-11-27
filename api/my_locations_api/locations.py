from sanic_ext import validate
from sanic import Blueprint, HTTPResponse, Request
from sanic.response import empty, json
from sanic.views import HTTPMethodView

from my_locations_api.validators import LocationItemBase, LocationItem, MapBounds


locations_blueprint = Blueprint("Location", url_prefix="/locations")


class LocationView(HTTPMethodView):

    @validate(query=MapBounds)
    async def get(
        self,
        request: Request,
        query: MapBounds
    ) -> HTTPResponse:
        return json({ "location": "get" })

    @validate(query=MapBounds)
    async def head(
        self,
        request: Request,
        query: MapBounds
    ) -> HTTPResponse:
        return await self.get(request)

    @validate(json=LocationItem)
    async def post(
        self,
        request: Request,
        body: LocationItem
    ) -> HTTPResponse:
        return json({ "location": "post" })


class LocationItemView(HTTPMethodView):

    async def get(self, request: Request, id: int) -> HTTPResponse:
        return json({ "location": id })

    async def head(self, request: Request, id: int) -> HTTPResponse:
        return await self.get(request, id)

    @validate(json=LocationItemBase)
    async def patch(
        self,
        request: Request,
        id: int,
        body: LocationItemBase
    ) -> HTTPResponse:
        return json({ "patch": id })

    async def delete(self, request: Request, id: int):
        return json({ "delete": id })


locations_blueprint.add_route(
    LocationView.as_view(),
    "/",
    version=1,
    error_format="json",
)

locations_blueprint.add_route(
    LocationItemView.as_view(),
    "/<id:int>",
    version=1,
    error_format="json",
)
