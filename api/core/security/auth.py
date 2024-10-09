from logging import getLogger
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from core.database.base import get_db_session
from core.database.models.user import UserModel
from core.security.jwt import decode_and_validate_token


logger = getLogger(__name__)

async def get_current_user(
    payload: dict = Depends(decode_and_validate_token),
    db: Session = Depends(get_db_session)
) -> UserModel:
    auth0_id: str = payload.get("sub")
    if auth0_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    result = await db.execute(select(UserModel).filter(UserModel.auth0_id == auth0_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user)
) -> UserModel:
    """
    Get the current active user.

    Args:
        current_user (User): The current user.

    Returns:
        User: The current active user.

    Raises:
        HTTPException: If the user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


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
