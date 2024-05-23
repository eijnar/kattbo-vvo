from fastapi import Depends
from core.security.auth import get_current_active_user, check_scopes

def get_user_and_check_scopes(required_scope: str):
    """
    Dependency to get the current active user and check the required scope.

    Args:
        required_scope (str): The required scope.

    Returns:
        Callable: A dependency function.
    """
    def dependency(
        current_user = Depends(get_current_active_user),
        payload = Depends(lambda: check_scopes(required_scope))
    ):
        return current_user
    return dependency
