from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.dependencies import get_db_session
from core.security.token_manager import TokenManager, get_token_manager
from core.security.redis_client import get_redis_client_for_unconfirmed_users
from services.user_service import UserService

async def get_user_service(
    db_session: AsyncSession = Depends(get_db_session),
    token_manager: TokenManager = Depends(get_token_manager),
    redis_client = Depends(get_redis_client_for_unconfirmed_users)
) -> UserService:
    return UserService(db_session, token_manager, redis_client)