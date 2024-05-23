from typing import Annotated, Union

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes


from core.security.scopes import scopes
from core.security.schemas import TokenDataSchema
from core.security.passwords import verify_password
from core.security.token_manager import TokenManager, get_token_manager
from core.database.models import UserModel 
from repositories.user_repository import UserRepository
from core.dependencies.user_repository import get_user_repository
from schemas.user import UserBaseSchema


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token", scopes=scopes)



async def authenticate_user(
    email: str, 
    password: str, 
    user_repository: UserRepository = Depends(get_user_repository)
):
    """
    Authenticate user by email and password.

    Args:
        email (str): The user's email.
        password (str): The user's password.
        user_repository (UserRepository): The user repository to retrieve user information.

    Returns:
        Union[UserModel, None]: The authenticated user or None if authentication fails.
    """
    user = await user_repository.get_user_by_email(email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def get_current_user(
    request: Request,
    security_scopes: SecurityScopes,
    user_repository: UserRepository = Depends(get_user_repository),
    token_manager: TokenManager = Depends(get_token_manager),
) -> UserModel:
    """
    Get the current user from the token.

    Args:
        security_scopes (SecurityScopes): The security scopes.
        user_repository (UserRepository): The user repository.
        token_manager (TokenManager): The token manager.
        token (str): The token.

    Returns:
        UserModel: The current user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": f"Bearer"}
        )

    try:
        payload = await token_manager.validate_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSchema(scopes=token_scopes, user_id=user_id)
    except Exception as e:  # Assuming JWTError is the error class used in your token manager
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from e

    user = await user_repository.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if security_scopes.scopes:
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                    headers={"WWW-Authenticate": f"Bearer scope=\"{security_scopes.scope_str}\""}
                )

    return user



async def get_current_active_user(
    current_user: Annotated[UserBaseSchema, Depends(get_current_user)]
) -> UserBaseSchema:
    """
    Get the current active user.

    Args:
        current_user (UserBaseSchema): The current user.

    Returns:
        UserBaseSchema: The current active user.

    Raises:
        HTTPException: If the user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
