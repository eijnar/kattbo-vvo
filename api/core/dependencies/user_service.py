from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.user_repository import get_db_session
from services.user_service import UserService


async def get_user_service(
    db_session: AsyncSession = Depends(get_db_session)
) -> UserService:
    return UserService(db_session)
