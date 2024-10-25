from logging import getLogger
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader

from core.security.jwt import decode_and_validate_token
from core.security.security_service import SecurityService
from core.dependencies import get_security_service
from core.security.models import UserContext


logger = getLogger(__name__)
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(
    security_service: SecurityService = Depends(get_security_service),
    token: Optional[str] = Depends(oauth2_scheme),
    api_key: Optional[str] = Depends(api_key_header),
) -> UserContext:
    """
    Dependency to get the current authenticated user and their permissions.
    """
    user_context = None
    logger.debug("get_current_user called")

    if token:
        logger.debug("Token provided")
        try:
            user_context = await security_service.authenticate_with_token(token=token)
            logger.info(f"User authenticated via OAuth2 token.", extra={'user.id': str(user_context.user.id)})
        except HTTPException as e:
            logger.warning(f"OAuth2 authentication failed: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during token authentication: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OAuth2 token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif api_key:
        logger.debug("API key provided")
        try:
            user_context = await security_service.authenticate_with_api_key(api_key=api_key)
            logger.info(f"User authenticated via API Key.", extra={'user.id': str(user_context.user.id)})
        except HTTPException as e:
            logger.warning(f"API Key authentication failed: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error during API Key authentication: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )

    if not user_context:
        logger.warning("No authentication credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_context


def get_current_active_user(required_scope: Optional[str] = None):
    async def dependency(
        user_context: UserContext = Depends(get_current_user)
    ) -> UserContext:
        logger.debug("get_current_active_user called")
        user = user_context.user

        # Check if user is active (not disabled)
        if user.disabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        # Check for required scopes if any
        if required_scope:
            if not user_context.has_permission(required_scope):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )

        return user_context

    return dependency


def requires_scope(required_scope: Optional[str] = None):
    async def dependency(
        payload: dict = Depends(decode_and_validate_token)
    ):
        if required_scope:
            # Collect scopes from 'scope' and 'permissions'
            scopes = set()
            if 'scope' in payload:
                scopes.update(payload['scope'].split())
            if 'permissions' in payload:
                scopes.update(payload['permissions'])
            if required_scope not in scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
        return payload
    return dependency