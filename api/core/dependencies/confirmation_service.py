from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies.user_repository import get_db_session
from core.security.token_manager import TokenManager, get_token_manager_for_unconfirmed_users
from core.redis.client import get_redis_client_for_unconfirmed_users
from services.confirmation_service import ConfirmationService


async def get_confirmation_service(
    db_session: AsyncSession = Depends(get_db_session),
    token_manager: TokenManager = Depends(
        get_token_manager_for_unconfirmed_users),
    redis_client=Depends(get_redis_client_for_unconfirmed_users)
) -> ConfirmationService:
    return ConfirmationService(db_session, token_manager, redis_client)
