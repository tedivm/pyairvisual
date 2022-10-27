"""Define tests for API requests and responses."""
import json

import aiohttp
import pytest

from pyairvisual import CloudAPI

from tests.common import (
    TEST_API_KEY,
    TEST_CITY,
    TEST_COUNTRY,
    TEST_LATITUDE,
    TEST_LONGITUDE,
    TEST_NODE_ID,
    TEST_STATE,
    TEST_STATION_NAME,
)


@pytest.mark.asyncio
async def test_aqi_ranking(aresponses, city_ranking_response):
    """Test getting AQI ranking by city."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_ranking_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.ranking()
        assert len(data) == 3
        assert data[0]["city"] == "Portland"
        assert data[0]["state"] == "Oregon"
        assert data[0]["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_cities(aresponses, cities_response):
    """Test getting a list of supported cities."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/cities",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(cities_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.cities(TEST_COUNTRY, TEST_STATE)
        assert len(data) == 27

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_coordinates(aresponses, city_response):
    """Test getting the nearest city by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_city(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )
        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_ip(aresponses, city_response):
    """Test getting the nearest city by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_city()
        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_city_by_name(aresponses, city_response):
    """Test getting a city by its name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.city(
            city=TEST_CITY, state=TEST_STATE, country=TEST_COUNTRY
        )

        assert data["city"] == "Los Angeles"
        assert data["state"] == "California"
        assert data["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_countries(aresponses, countries_response):
    """Test getting a list of supported countries."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/countries",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(countries_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.countries()
        assert len(data) == 79

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_no_explicit_client_session(aresponses, city_ranking_response):
    """Test not explicitly providing an aiohttp ClientSession."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/city_ranking",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(city_ranking_response), status=200
        ),
    )

    cloud_api = CloudAPI(TEST_API_KEY)
    data = await cloud_api.air_quality.ranking()
    assert len(data) == 3
    assert data[0]["city"] == "Portland"
    assert data[0]["state"] == "Oregon"
    assert data[0]["country"] == "USA"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_node_by_id(aresponses, node_by_id_response):
    """Test getting a node's info by its ID from the cloud API."""
    aresponses.add(
        "www.airvisual.com",
        "/api/v2/node/12345",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(node_by_id_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.node.get_by_node_id(TEST_NODE_ID)
        assert data["current"]["tp"] == 2.3
        assert data["current"]["hm"] == 73
        assert data["current"]["p2"] == 35
        assert data["current"]["co"] == 479

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_states(aresponses, states_response):
    """Test getting a list of supported states."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/states",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(states_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.states(TEST_COUNTRY)
        assert len(data) == 6

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_coordinates(aresponses, station_response):
    """Test getting a station by latitude and longitude."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_station(
            latitude=TEST_LATITUDE, longitude=TEST_LONGITUDE
        )
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_ip(aresponses, station_response):
    """Test getting a station by IP address."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/nearest_station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.nearest_station()
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_station_by_name(aresponses, station_response):
    """Test getting a station by location name."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/station",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(station_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.air_quality.station(
            station=TEST_STATION_NAME,
            city=TEST_CITY,
            state=TEST_STATE,
            country=TEST_COUNTRY,
        )
        assert data["city"] == "Beijing"
        assert data["state"] == "Beijing"
        assert data["country"] == "China"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_stations(aresponses, stations_response):
    """Test getting a list of supported stations."""
    aresponses.add(
        "api.airvisual.com",
        "/v2/stations",
        "get",
        response=aiohttp.web_response.json_response(
            json.loads(stations_response), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        cloud_api = CloudAPI(TEST_API_KEY, session=session)
        data = await cloud_api.supported.stations(TEST_CITY, TEST_STATE, TEST_COUNTRY)
        assert len(data) == 2

    aresponses.assert_plan_strictly_followed()
