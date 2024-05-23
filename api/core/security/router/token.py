import logging
from datetime import timedelta

from fastapi import Depends, status, HTTPException, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from elasticapm import set_transaction_outcome

from core.security.schemas import TokenSchema
from core.security.auth import authenticate_user
from core.security.token_manager import TokenManager, get_token_manager
from core.dependencies.user_repository import get_user_repository
from repositories.user_repository import UserRepository
from core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    response: Response,
    user_repository: UserRepository = Depends(get_user_repository),
    form_data: OAuth2PasswordRequestForm = Depends(),
    token_manager: TokenManager = Depends(get_token_manager)
):
    user = await authenticate_user(
        email=form_data.username,
        password=form_data.password,
        user_repository=user_repository
    )
    if not user:
        logger.warning(
            f"Failed login attempt by someone using this email: {form_data.username}"
        )
        set_transaction_outcome('failure')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scopes = await user_repository.get_user_scopes(user.id)

    access_token_lifespan = timedelta(
        minutes=settings.ACCESS_TOKEN_LIFESPAN_MINUTES
    )
    refresh_token_lifespan = timedelta(
        days=settings.REFRESH_TOKEN_LIFESPAN_DAYS
    )

    access_token = await token_manager.create_token(
        user_id=user.id,
        token_type="access",
        scopes=scopes,
        expires_delta=access_token_lifespan,
    )

    refresh_token = await token_manager.create_token(
        user_id=user.id,
        token_type="refresh",
        expires_delta=refresh_token_lifespan,
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Ensure this is set to True in production
        samesite="Strict",
        max_age=access_token_lifespan.total_seconds()
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # Ensure this is set to True in production
        samesite="Strict",
        max_age=refresh_token_lifespan.total_seconds()
    )

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_lifespan.total_seconds(),
        refresh_token=refresh_token
    )
