"""Define tests for API errors."""
import json
from unittest.mock import Mock

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from pyairvisual.cloud_api import (
    AirVisualError,
    CloudAPI,
    InvalidKeyError,
    KeyExpiredError,
    LimitReachedError,
    NoStationError,
    NotFoundError,
    UnauthorizedError,
)
from tests.common import TEST_API_KEY


@pytest.mark.asyncio
async def test_invalid_json_response(aresponses: ResponsesMockServer) -> None:
    """Test that the proper error is raised when the response text isn't JSON.

    Args:
        aresponses: A callable that returns a ResponsesMockServer.
    """
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        aresponses.Response(
            text="This is a valid response, but it isn't JSON.",
            headers={"Content-Type": "application/json"},
            status=200,
        ),
    )

    with pytest.raises(AirVisualError):
        async with aiohttp.ClientSession() as session:
            cloud_api = CloudAPI(TEST_API_KEY, session=session)
            await cloud_api.node.get_by_node_id("12345")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_text_fixture,status_code,exception",
    [
        ("error_city_not_found_response", 400, NotFoundError),
        ("error_forbidden_response", 403, UnauthorizedError),
        ("error_generic_response", 404, AirVisualError),
        ("error_incorrect_api_key_response", 401, InvalidKeyError),
        ("error_key_expired_response", 401, KeyExpiredError),
        ("error_limit_reached_response", 429, LimitReachedError),
        ("error_no_nearest_station_response", 404, NoStationError),
        ("error_node_not_found_response", 404, NotFoundError),
        ("error_payment_required_response", 403, InvalidKeyError),
        ("error_permission_denied_response", 403, UnauthorizedError),
    ],
)
async def test_errors(
    aresponses: ResponsesMockServer,
    exception: type[AirVisualError],
    request: Mock,
    response_text_fixture: str,
    status_code: int,
) -> None:
    """Test various cloud API errors.

    Args:
        aresponses: An aresponses server.
        exception: An API exception.
        request: The pytest request fixture.
        response_text_fixture: The fixture that returns an API response payload.
        status_code: A response status code.
    """
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(request.getfixturevalue(response_text_fixture)),
            status=status_code,
        ),
    )

    with pytest.raises(exception):
        async with aiohttp.ClientSession() as session:
            cloud_api = CloudAPI(TEST_API_KEY, session=session)
            await cloud_api.air_quality.nearest_city()
