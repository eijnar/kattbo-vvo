import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserBaseSchema
from core.security.token_manager import TokenManager
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: AsyncSession, token_manager: TokenManager, redis_client):
        self.user_repository = UserRepository(db_session)
        self.token_manager = token_manager
        self.redis_client = redis_client

    async def get_all_users(self, page: int, page_size: int) -> List[UserBaseSchema]:
        try:
            users = await self.user_repository.get_all_users(page=page, page_size=page_size)
            return users
        except Exception as e:
            logger.error(f"Failed to fetch users: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch users")
