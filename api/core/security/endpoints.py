from datetime import timedelta

from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import TokenSchema
from .auth import authenticate_user
from .oauth import get_user_scopes
from .token_manager import TokenManager
from core.database import get_db
from core.config import settings


security = APIRouter()

@security.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    token_manager: TokenManager = Depends(TokenManager.create)
):

    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = await get_user_scopes(user.id, db)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRES_DAYS)
    
    access_token = await token_manager.create_access_token(
        user_id=user.id,
        expires_delta=access_token_expires,
        scopes=scopes
    )
    
    refresh_token = await token_manager.create_refresh_token(
        user_id=user.id,
        expires_delta=refresh_token_expires
    )
    
    return {       
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),
        "refresh_token": refresh_token
        }
