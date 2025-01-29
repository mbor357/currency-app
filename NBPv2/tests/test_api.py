import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
import pytest_asyncio
import httpx
from database import database

@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():

    await database.connect()
    yield
    await database.disconnect()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.ASGITransport(app),
    ) as client:
        yield client

@pytest.mark.parametrize(
    "start_date, end_date, expected_status",
    [
        ("2024-01-01", "2024-01-31", 200),   # Poprawne daty
        ("2024-02-30", "2023-03-01", 422),   # Błędna data
        ("invalid-date", "2023-03-01", 422), # Format niepoprawny
        (None, None, 422),  # Brak daty
    ]
)
@pytest.mark.asyncio
async def test_fetch_and_save_currencies(async_client, start_date, end_date, expected_status):
    response = await async_client.post(
        "/currencies/fetch",
        params={"start_date": start_date, "end_date": end_date},
    )
    assert response.status_code == expected_status

@pytest.mark.asyncio
async def test_get_currencies(async_client):
    response = await async_client.get("/currencies?start_date=2024-01-01&end_date=2024-01-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_currencies_by_year(async_client):
    response = await async_client.get("/currencies/year/2024")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_currencies_by_quarter(async_client):
    response = await async_client.get("/currencies/quarter/2024/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_currencies_by_month(async_client):
    response = await async_client.get("/currencies/month/2024/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_currencies_by_day(async_client):
    response = await async_client.get("/currencies/day/2024/01/03")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
