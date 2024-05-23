import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserBaseSchema
from repositories.user_repository import UserRepository

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
