from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security.auth import get_current_active_user, check_scopes
from core.security.jwt import decode_jwt

http_bearer = HTTPBearer()

def get_user_and_check_scopes(required_scope: str):
    """
    Dependency to get the current active user and check the required scope.

    Args:
        required_scope (str): The required scope.

    Returns:
        Callable: A dependency function.
    """
    async def dependency(
        current_user = Depends(get_current_active_user),
        payload = Depends(lambda: check_scopes(required_scope))
    ):
        return current_user
    return dependency

def requires_scope(required_scope: str):
    async def dependency(credentials: HTTPAuthorizationCredentials = Security(http_bearer)):
        token = credentials.credentials
        payload = decode_jwt(token)
        token_scopes = payload.get('scope', '').split()
        if required_scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return payload
    return dependency