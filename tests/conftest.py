import pytest
from httpx import AsyncClient
from app.routes import app

@pytest.fixture()
async def ac():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac