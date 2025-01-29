import pytest
from httpx import AsyncClient
from main import app  # Upewnij się, że importujesz swoją FastAPI app poprawnie

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client