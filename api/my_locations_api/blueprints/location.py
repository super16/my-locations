from typing import TYPE_CHECKING, Optional

from sanic import Blueprint, HTTPResponse, Request
from sanic.exceptions import BadRequest, NotFound, ServerError
from sanic.response import empty, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sqlalchemy import delete, insert, select, update

if TYPE_CHECKING:
    from sqlalchemy.engine import Result, ScalarResult
    from sqlalchemy.ext.asyncio import AsyncSession

from my_locations_api.models.location import Location
from my_locations_api.validators import (
    LocationItem,
    LocationItemBase,
    MapBounds,
    invalid_location_item_fields,
)

locations_blueprint = Blueprint("Location", url_prefix="/locations")


class LocationView(HTTPMethodView):
    """Class to get an array of locations for given map bounds."""

    @validate(query=MapBounds)
    async def get(
        self,
        request: Request,
        query: MapBounds,
    ) -> HTTPResponse:
        """Get list of locations by map bounds.

        openapi:
        ---
        parameters:
          - name: end_latitude
            in: query
            required: true
            schema:
              type: number
          - name: end_longitude
            in: query
            required: true
            schema:
              type: number
          - name: start_latitude
            in: query
            required: true
            schema:
              type: number
          - name: start_longitude
            in: query
            required: true
            schema:
              type: number
        responses:
          '200':
            description: List of locations or empty list.
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            db_query = select(Location).where(
                Location.latitude.between(
                    query.start_latitude,
                    query.end_latitude,
                ),
            ).where(
                Location.longitude.between(
                    query.start_longitude,
                    query.end_longitude,
                ),
            )
            result: Result = await session.execute(db_query)
            locations: ScalarResult[Location] = result.scalars()

        if not locations:
            return empty()

        return json([loc.serialize() for loc in locations])

    @validate(query=MapBounds)
    async def head(
        self,
        request: Request,
        query: MapBounds,
    ) -> HTTPResponse:
        """Headers of locations request by map bounds.

        openapi:
        ---
        parameters:
          - name: end_latitude
            in: query
            required: true
            schema:
              type: number
          - name: end_longitude
            in: query
            required: true
            schema:
              type: number
          - name: start_latitude
            in: query
            required: true
            schema:
              type: number
          - name: start_longitude
            in: query
            required: true
            schema:
              type: number
        responses:
          '200':
            description: Headers of locations request.
        """
        return await self.get(request, query)

    @validate(json=LocationItem)
    async def post(
        self,
        request: Request,
        body: LocationItem,
    ) -> HTTPResponse:
        """Create new location.

        openapi:
        ---
        consumes:
          - application/json
        requestBody:
          content:
            application/json:
              schema:
                type: object
              example:
                title: "My new location"
                description: "Description of new location"
                latitude: 5.565333
                longitude: 5.998989
        responses:
          '201':
            description: Location has been created.
        """
        invalid_fields = invalid_location_item_fields(body)
        if invalid_fields:
            error_message = "Input should not be empty"
            raise BadRequest(
                error_message,
                context={"invalid_fields": invalid_fields},
            )

        session: AsyncSession = request.ctx.session
        async with session.begin():
            db_query = insert(Location).values(
                title=body.title,
                description=body.description,
                latitude=body.latitude,
                longitude=body.longitude,
            ).returning(Location)

            result: Result = await session.execute(db_query)
            created_location: Optional[Location] = result.scalar()

        if not created_location:
            error_message = "Can't create location"
            raise ServerError(error_message)

        return json(created_location.serialize())


class LocationItemView(HTTPMethodView):

    async def get(self, request: Request, location_id: int) -> HTTPResponse:
        """Get location by id.

        openapi:
        ---
        parameters:
        - in: path
          name: location_id
        responses:
          '200':
            description: Location has been deleted.
          '404':
            description: Location has not been found.
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            db_query = select(Location).where(
                Location.location_id == location_id,
            )
            result: Result = await session.execute(db_query)
            location: Optional[Location] = result.scalar()

        if not location:
            error_message = "Location has not been found"
            raise NotFound(error_message)

        return json(location.serialize())

    async def head(self, request: Request, location_id: int) -> HTTPResponse:
        """Headers of location by id.

        openapi:
        ---
        parameters:
        - in: path
          name: location_id
        responses:
          '200':
            description: Headers returned.
        """
        return await self.get(request, location_id)

    @validate(json=LocationItemBase)
    async def patch(
        self,
        request: Request,
        location_id: int,
        body: LocationItemBase,
    ) -> HTTPResponse:
        """Update location by id.

        openapi:
        ---
        parameters:
        - in: path
          name: location_id
        requestBody:
          content:
            application/json:
              schema:
                type: object
              example:
                title: "New location title"
                description: "New location description"
        responses:
          '200':
            description: Location has been updated.
          '404':
            description: Location has not been found.
        """
        invalid_fields = invalid_location_item_fields(body)
        if invalid_fields:
            error_message = "Input should not be empty"
            raise BadRequest(
                error_message,
                context={"invalid_fields": invalid_fields},
            )

        session: AsyncSession = request.ctx.session
        async with session.begin():
            db_query = update(Location).where(
                Location.location_id == location_id,
            ).values(
                title=body.title, description=body.description,
            ).returning(Location)

            result: Result = await session.execute(db_query)
            updated_location: Optional[Location] = result.scalar()

        if not updated_location:
            error_message = "Location has not been found"
            raise NotFound(error_message)

        return json(updated_location.serialize())

    async def delete(self, request: Request, location_id: int) -> HTTPResponse:
        """Delete location by id.

        openapi:
        ---
        parameters:
        - in: path
          name: location_id
        responses:
          '204':
            description: Location has been deleted.
        """
        session: AsyncSession = request.ctx.session
        async with session.begin():
            await session.execute(
                delete(Location).where(
                  Location.location_id == location_id,
                ),
            )

        return empty()


locations_blueprint.add_route(
    LocationView.as_view(),
    "/",
    version=1,
    error_format="json",
)

locations_blueprint.add_route(
    LocationItemView.as_view(),
    "/<location_id:int>",
    version=1,
    error_format="json",
)
