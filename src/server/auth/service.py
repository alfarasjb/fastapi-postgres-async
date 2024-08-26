import logging

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from src.server.auth import schemas, models

logger = logging.getLogger(__name__)

# Note: Use Schemas for arguments, and Map the schemas to models.
# Note: session.query does not exist for AsyncSession.


class AuthService:
    """ 
    Auth Crud Service
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self):
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

    async def create_user(self, user: schemas.User):
        user_model = models.User(name=user.name, email=user.email)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user

    async def get_user_by_id(self, user_id: int):
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalars().first()
        return user

    async def delete_user_by_id(self, user_id: int):
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.first()
        await self.session.delete(user)
        await self.session.commit()
