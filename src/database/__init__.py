from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from src.config.credentials import Credentials
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)
# Used in db models
Base = declarative_base()

DATABASE_URL = Credentials.database_url()

async_engine = create_async_engine(url=Credentials.database_url())


async def init_db():
    """Create database tables"""
    try:
        async with async_engine.begin() as conn:
            # Import the models to register them with SQLAlchemy
            from src.server.auth.models import User
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.error(f"An error occurred initializing database. Error: {e}", exc_info=True)
        raise


async def cleanup():
    await async_engine.dispose()


async def get_session() -> AsyncSession:
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
