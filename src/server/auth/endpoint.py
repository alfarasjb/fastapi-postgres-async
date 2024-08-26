from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.server.auth import schemas
import logging
from src.server.auth.service import AuthService
from src.database import get_session

logger = logging.getLogger(__name__)

api = APIRouter()


@api.post("/api/create-user", response_model=schemas.User)
async def create_user(user: schemas.User, session: AsyncSession = Depends(get_session)):
    try:
        logger.info(f"Creating user. Email: {user.email} Name: {user.name}")
        service = AuthService(session=session)
        created_user = await service.create_user(user=user)
        return created_user
    except Exception as e:
        err_msg = f"Failed to create user. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.get("/api/get-users")
async def get_users(session: AsyncSession = Depends(get_session)):
    try:
        logger.info(f"Getting all users")
        service = AuthService(session=session)
        all_users = await service.get_all_users()
        return all_users
    except Exception as e:
        err_msg = f"Failed to get all users. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.get("/api/get-user/<user_id>")
async def get_user_by_user_id(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        logger.info(f"Getting User by ID. ID: {user_id}")
        service = AuthService(session=session)
        user = await service.get_user_by_id(user_id=user_id)
        return user
    except Exception as e:
        err_msg = f"Failed to get user by user id. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)
