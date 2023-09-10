from pytest import mark
from sanic import Sanic
from ujson import loads


@mark.asyncio
async def test_get_locations_list(app: Sanic, get_locations_path: str):
    _, response = await app.asgi_client.get(get_locations_path)
    assert response.status == 200


@mark.asyncio
async def test_create_standalone_location(
    app: Sanic,
    standalone_single_location: tuple[str, dict[str, float | str]],
):
    # Create location
    get_locations_path, new_location = standalone_single_location
    _, post_response = await app.asgi_client.post(
        "/v1/locations",
        json=new_location,
    )
    assert post_response.status == 200

    # Get locations and check if it contains created location
    _, get_response = await app.asgi_client.get(get_locations_path)
    assert get_response.status == 200
    assert len(loads(get_response.body)) == 1


@mark.asyncio
async def test_crud_location(
    app: Sanic,
    new_location: dict[str, float | str],
    get_locations_path: str,
    update_for_location: dict[str, str],
):
    # Create location
    _, post_response = await app.asgi_client.post(
        "/v1/locations",
        json=new_location,
    )
    assert post_response.status == 200

    # Get locations and get added location
    _, get_response = await app.asgi_client.get(get_locations_path)
    assert get_response.status == 200
    response_body: list[dict] = loads(get_response.body)
    assert len(response_body) == 1

    # Check if location were added correctly
    added_location = response_body[0]
    added_location_id = added_location.get("id")

    for k in new_location.keys():
        assert new_location.get(k) == added_location.get(k)

    # Update added location
    _, patch_response = await app.asgi_client.patch(
        f"/v1/locations/{added_location_id}",
        json=update_for_location,
    )
    assert patch_response.status == 200

    # Get location and check if location were updated correctly
    _, get_response = await app.asgi_client.get(get_locations_path)
    response_body = loads(get_response.body)
    updated_location = response_body[0]
    for k in update_for_location.keys():
        assert updated_location.get(k) == updated_location.get(k)

    # Delete the location and check if location is not there anymore
    _, delete_response = await app.asgi_client.delete(
        f"/v1/locations/{added_location_id}",
    )
    assert delete_response.status == 204

    _, get_response = await app.asgi_client.get(get_locations_path)
    response_body = loads(get_response.body)
    assert len(response_body) == 0
