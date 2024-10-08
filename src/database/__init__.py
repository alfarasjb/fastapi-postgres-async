import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import SETTINGS

logger = logging.getLogger(__name__)
# Used in db models

# DATABASE_URL = Credentials.database_url()
DATABASE_URL = SETTINGS.ASYNC_POSTGRES_URI
print(f"DB URL: {type(DATABASE_URL)}")
async_engine = create_async_engine(url=DATABASE_URL)

# NOTE: In the future, consider using SQLModel https://sqlmodel.tiangolo.com/ since it's built on top of SQLAlchemy and Pydantic


async def init_db():
    """Create database tables"""
    try:
        async with async_engine.begin() as conn:
            # Import the models to register them with SQLAlchemy
            from src.server.auth.models import User
            # await conn.run_sync(Base.metadata.create_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        logger.error(f"An error occurred initializing database. Error: {e}", exc_info=True)
        raise


async def cleanup():
    await async_engine.dispose()


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
