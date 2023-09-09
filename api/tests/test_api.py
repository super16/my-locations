from pytest import mark
from sanic import Sanic


@mark.asyncio
async def test_get_locations_list(app: Sanic, map_bounds: dict[str, float]):
    get_locations_path = (
        "/v1/locations?"
        f"end_latitude={map_bounds.get('end_latitude')}&"
        f"end_longitude={map_bounds.get('end_longitude')}&"
        f"start_latitude={map_bounds.get('start_latitude')}&"
        f"start_longitude={map_bounds.get('start_longitude')}"
    )
    request, response = await app.asgi_client.get(get_locations_path)
    assert response.status == 200
