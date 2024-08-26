import logging
from typing import Optional, Sequence

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.server.auth import schemas, models
from src.server.auth.service import AuthService
from src.server.auth.constants import *

logger = logging.getLogger(__name__)

api = APIRouter()


@api.post(CREATE_USER_ROUTE, response_model=schemas.User)
async def create_user(
        user: schemas.User, session: AsyncSession = Depends(get_session)
) -> Optional[models.User]:
    try:
        logger.info(f"Creating user. Email: {user.email} Name: {user.name}")
        service = AuthService(session=session)
        created_user = await service.create_user(user=user)
        return created_user
    except Exception as e:
        err_msg = f"Failed to create user. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.get(GET_USERS_ROUTE)
async def get_users(
        session: AsyncSession = Depends(get_session)
) -> Optional[Sequence[models.User]]:
    try:
        logger.info(f"Getting all users")
        service = AuthService(session=session)
        all_users = await service.get_all_users()
        return all_users
    except Exception as e:
        err_msg = f"Failed to get all users. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.get(GET_USER_BY_USER_ID_ROUTE)
async def get_user_by_user_id(
        user_id: int, session: AsyncSession = Depends(get_session)
) -> Optional[models.User]:
    try:
        logger.info(f"Getting User by ID. ID: {user_id}")
        service = AuthService(session=session)
        user = await service.get_user_by_id(user_id=user_id)
        return user
    except Exception as e:
        err_msg = f"Failed to get user by user id. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.post(UPDATE_USER_ROUTE, response_model=schemas.User)
async def update_user(
        user_id: int, user: schemas.User, session: AsyncSession = Depends(get_session)
) -> Optional[models.User]:
    try:
        logger.info(f"Updating User. Name: {user.name} Email: {user.email}")
        service = AuthService(session=session)
        updated_user = await service.update_user_by_id(user_id=user_id, user=user)
        return updated_user
    except Exception as e:
        err_msg = f"Failed to update user. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)


@api.post(DELETE_USER_ROUTE)
async def delete_user(
        user_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    try:
        logger.info(f"Deleting User. ID: {user_id}")
        service = AuthService(session=session)
        await service.delete_user_by_id(user_id=user_id)
    except Exception as e:
        err_msg = f"Failed to delete user. An unknown error occurred."
        logger.error(f"{err_msg} Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=err_msg)
