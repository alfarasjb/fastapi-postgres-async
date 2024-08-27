import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import SETTINGS
from src.database import get_session
from src.main import app
from src.server.auth.constants import *

# Run pytest --disable-warnings -s
# TODO: Fix the tests

DATABASE_URL = SETTINGS.ASYNC_POSTGRES_URI

engine = create_async_engine(
    DATABASE_URL,
    poolclass=StaticPool
)


async def override_get_session():
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

client = TestClient(app)

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="module", autouse=True)
async def prepare_database():
    """Fixture to initialize and clean up db"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_user():
    response = client.post(CREATE_USER_ROUTE, json={"name": "test_name", "email": "test_email"})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == "test_name"
    assert data['email'] == "test_email"


@pytest.mark.asyncio
async def test_get_users():
    response = client.get(GET_USERS_ROUTE)
    print(response.status_code)
    assert response.status_code == 200


"""
def test_get_user_by_user_id():
    pass


def test_update_user():
    pass


def test_delete_user():
    pass
"""