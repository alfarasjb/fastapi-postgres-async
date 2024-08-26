from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.database import Base, init_db
from src.config import SETTINGS
import pytest
from src.main import app



DATABASE_URL = SETTINGS.TEST_POSTGRES_URI

async_engine = create_async_engine(url=DATABASE_URL)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

@pytest.fixture()
async def test_db():
    try:
        async with async_engine.begin() as conn:
            from src.server.auth.models import User
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        pass

app.dependency_overrides[init_db] = get_session

client = TestClient(app)


def test_get_users(test_db):
    response = client.get("/api/get-users")
    assert response.status_code == 200
