from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from core.database.base import get_db_session
from core.database.models.user import UserModel
from core.security.jwt import decode_jwt
from core.security.schemas import TokenPayload


# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
) -> UserModel:
    """
    Get the current user from the token.

    Args:
        token (str): The token.
        db (Session): The database session.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = decode_jwt(token)
        auth0_id: str = payload.get("sub")
        if auth0_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(UserModel).filter(UserModel.auth0_id == auth0_id).first()
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


def check_scopes(required_scope: str, token: str = Depends(oauth2_scheme)):
    """
    Check if the token has the required scope.

    Args:
        required_scope (str): The required scope.
        token (str): The token.

    Returns:
        dict: The token payload.

    Raises:
        HTTPException: If the token does not have the required scope.
    """
    payload = decode_jwt(token)
    if 'scope' not in payload or required_scope not in payload['scope'].split():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return payload

async def verify_auth0_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Validate the Auth0 token and get the user payload.

    Args:
        token (str): The JWT token from the request.

    Returns:
        TokenPayload: The payload of the token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    payload = decode_jwt(token)
    return TokenPayload(**payload)