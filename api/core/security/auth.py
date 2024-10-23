from logging import getLogger
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from core.dependencies import get_db_session
from core.database.models.user import UserModel
from core.security.jwt import decode_and_validate_token
from core.security.service import SecurityService


logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    security_service: SecurityService = Depends(get_security_service),
    token: Optional[str] = Depends(oauth2_scheme),
    api_key: Optional[str] = Depends(api_key_scheme),
    db: Session = Depends(get_db_session),
    required_scope: Optional[str] = None
) -> UserModel:
    """
    Dependency to get the current active user based on either an Auth0 token or an API Key.
    Also checks for required scopes if provided.
    """
    user = None

    # Authenticate using OAuth2 token
    if token:
        try:
            user = await security_service.authenticate_with_token(token=token, db=db)
            logger.info(f"User {user.username} authenticated via OAuth2 token.")
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

    # If no user authenticated via token, try API Key
    elif api_key:
        try:
            user = security_service.authenticate_with_api_key(api_key=api_key.credentials, db=db)
            logger.info(f"User {user.username} authenticated via API Key.")
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

    # If neither token nor API Key is provided
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check for required scopes if any
    if required_scope:
        if not security_service.has_permission(user, required_scope):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    # Check if user is active (not disabled)
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


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