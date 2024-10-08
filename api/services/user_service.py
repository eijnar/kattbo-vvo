import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserBaseSchema, UserCreateSchema
from repositories.user_repository import UserRepository
from core.database.models import UserModel

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.user_repository = UserRepository(db_session)

    async def get_all_users(self, page: int, page_size: int) -> List[UserBaseSchema]:
        try:
            users = await self.user_repository.get_all_users(page=page, page_size=page_size)
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch users")

    async def get_user_by_auth0_id(self, auth0_id: str) -> UserBaseSchema:
        try:
            user = await self.user_repository.get_by_auth0_id(auth0_id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            logger.error(
                f"Failed to fetch user by auth0_id: {auth0_id}. Error: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch user"
            )

    async def register_user(self, user: UserCreateSchema) -> UserModel:
        try:
            # Check if the user already exists
            existing_user = await self.user_repository.get_by_auth0_id(user.auth0_id)
            if existing_user:
                raise HTTPException(status_code=400, detail="User already registered")

            # Create new user
            new_user = UserModel(
                auth0_id=user.auth0_id,
                email=user.email,
                first_name=user.first_name,
                disabled=False
            )
            # Save to the repository
            return await self.user_repository.create_user(new_user)
        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            raise HTTPException(status_code=500, detail="Failed to register user")