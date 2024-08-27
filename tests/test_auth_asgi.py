import pytest
from async_asgi_testclient import TestClient
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.server.auth.constants import *


@pytest.fixture
async def client():
    host, port = "0.0.0.0", 8080
    transport = ASGITransport(app=app, client=(host, port))
    async with AsyncClient(
            transport=transport,
            base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(CREATE_USER_ROUTE, json={"name": "test_name", "email": "test_email"})
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert data['name'] == "test_name"
        assert data['email'] == "test_email"

@pytest.mark.asyncio
async def test_get_user_by_user_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        key = "<user_id>"
        route = GET_USER_BY_USER_ID_ROUTE.replace(key, "3")
        print(route)
        response = await ac.get(route)
        print(response.json())
        assert response.status_code == 200
