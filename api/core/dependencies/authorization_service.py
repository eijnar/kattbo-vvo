from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.base import get_db_session
from core.redis.client import get_redis_client_for_authorize
from core.security.services.auth_service import AuthorizationService


async def get_authorization_service(
    db_session: AsyncSession = Depends(get_db_session),
    redis_client=Depends(get_redis_client_for_authorize)
) -> AuthorizationService:
    """
    Get an instance of AuthorizationService.

    Args:
        db (AsyncSession): An asynchronous database session.
        redis_client (redis.Redis): A Redis client for storing authorization codes.

    Returns:
        AuthorizationService: An instance of AuthorizationService.
    """
    return AuthorizationService(db_session, redis_client)
