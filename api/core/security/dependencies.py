from logging import getLogger
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from core.security.auth import get_current_active_user, requires_scope


http_bearer = HTTPBearer()
logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_and_check_scopes(required_scope: Optional[str] = None):
    """
    Dependency to get the current active user and check the required scope.

    Args:
        required_scope (str): The required scope.

    Returns:
        Callable: A dependency function.
    """
    async def dependency(
        current_user=Depends(get_current_active_user),
        _: dict = Depends(requires_scope(required_scope))
    ):
        return current_user
    return dependency
