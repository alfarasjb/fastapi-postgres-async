import logging
from typing import Sequence
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from src.server.auth import schemas, models

logger = logging.getLogger(__name__)

# Note: Use Schemas for arguments, and Map the schemas to models.
# Note: session.query does not exist for AsyncSession.

""" 
Some more notes: 

1. Use Schemas for Arguments 
- Schemas are defined using Pydantic, and have Input Validation (Important) 
- DTO (Data Transfer Objects) - allows you to define what data is required from the client when creating or updating resources 

2. User Models for Database Interactions 
- ORM Mapping - Models represent the actual database tables and are used to interact with the database through SQLAlchemy. 
They define the structure of your database entities. 
- Database Operations - When performing CRUD operations, you will convert the validated SCHEMA (with pydantic) into Model instances, 
which can then be added, updated, or deleted, from the database. 
"""


class AuthService:
    """ 
    Auth Crud Service
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> Sequence[models.User]:
        """
        Get list of all users
        """
        logger.info(f"Getting All users")
        statement = select(models.User)
        result = await self.session.execute(statement)
        # Always get scalar. Otherwise, you will get a value error
        users = result.scalars().all()
        logger.info(f"Result: {users}")
        return users

    async def create_user(self, user: schemas.User) -> models.User:
        user_model = models.User(name=user.name, email=user.email)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model

    async def get_user_by_id(self, user_id: int) -> models.User:
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalars().first()
        return user

    async def delete_user_by_id(self, user_id: int) -> None:
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar()
        await self.session.delete(user)
        await self.session.commit()

    async def get_user_by_name(self, user_name: str) -> models.User:
        statement = select(models.User).where(models.User.name == user_name)
        result = await self.session.execute(statement)
        user = result.scalar().first()
        return user

    async def get_user_by_email(self, user_email: str) -> models.User:
        statement = select(models.User).where(models.User.email == user_email)
        result = await self.session.execute(statement)
        user = result.scalar().first()
        return user

    async def update_user(self, user: schemas.User):
        pass

    async def update_user_by_id(self, user_id: int, user: schemas.User) -> models.User:
        # TODO Make this more robust
        existing_user = await self.get_user_by_id(user_id=user_id)
        if existing_user:
            # User exists, then update
            existing_user.name = user.name
            existing_user.email = user.email
            self.session.add(existing_user)  # Add the updated user to the session
            await self.session.commit()
            await self.session.refresh(existing_user)
            return existing_user
