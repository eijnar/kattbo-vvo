import logging
from datetime import timedelta

from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from elasticapm import set_transaction_outcome
from core.logger.setup import apm_client
from .schemas import TokenSchema
from .auth import authenticate_user
from ..database.dependencies import get_user_repository
from ..database.repositories import UserRepository
from .token_manager import TokenManager
from core.config import settings


security = APIRouter()
logger = logging.getLogger(__name__)


@security.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    user_repository: UserRepository = Depends(get_user_repository),
    form_data: OAuth2PasswordRequestForm = Depends(),
    token_manager: TokenManager = Depends(TokenManager.create)
):

    user = await authenticate_user(
        email=form_data.username,
        password=form_data.password,
        user_repository=user_repository
    )
    if not user:
        logger.warning(
            f"Failed login attempt by someone using this email: {form_data.username}")
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

    set_transaction_outcome('success')

    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_lifespan.total_seconds(),
        refresh_token=refresh_token
    )
