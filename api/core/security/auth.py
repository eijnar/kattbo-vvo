from typing import Annotated

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from .scopes import scopes
from .schemas import TokenDataSchema, UserBaseSchema
from .passwords import verify_password
from .crud import get_user
from .token_manager import TokenManager, get_token_manager
from core.logger import logger
from core.database import get_db
from models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token", scopes=scopes)


async def authenticate_user(email: str, password: str, db: AsyncSession = Depends(get_db)):
    logger.debug(f"DB Type: {type(db)} | DB: {db}")
    statement = select(UserModel).where(UserModel.email == email)
    result = await db.execute(statement)
    user = result.scalars().first()

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    db: AsyncSession = Depends(get_db),
    token_manager: TokenManager = Depends(get_token_manager),
    token: str = Depends(oauth2_scheme)
) -> UserModel:
    
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": authenticate_value}
    )

    try:
        payload = await token_manager.validate_token(token)
        logger.debug("Getting e-mail")
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.debug("email is none")
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSchema(scopes=token_scopes, user_id=user_id)
    except HTTPException as e:
        logger.error(f"Token validatioin error: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers=e.headers
        ) from e

    user = await get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
                headers={"WWW-Authenticate": authenticate_value}
            )
    return user


async def get_current_active_user(
    current_user: Annotated[UserBaseSchema, Depends(get_current_user)]
) -> UserBaseSchema:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
