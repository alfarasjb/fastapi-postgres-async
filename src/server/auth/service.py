from sqlalchemy.ext.asyncio.session import AsyncSession
from src.server.auth import schemas, models
from sqlalchemy.future import select


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
        statement = select(models.User)
        result = await self.session.execute(statement)
        return result.all()

    async def create_user(self, user: schemas.User):
        user_model = models.User(name=user.name, email=user.email)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user

    async def get_user_by_id(self, user_id: int):
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        return result.first()

    async def delete_user_by_id(self, user_id: int):
        statement = select(models.User).where(models.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.first()
        await self.session.delete(user)
        await self.session.commit()
