import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Security, Query, Request
from sqlalchemy.exc import IntegrityError

from schemas import UserBaseSchema, UserCreateSchema
from core.security import get_current_active_user
from core.security.token_manager import TokenManager, get_token_manager
from core.database.dependencies import get_user_repository
from core.database.models import UserModel
from core.config import settings
from repositories.user_repository import UserRepository
from routers.limiter import limiter
from services.confirmation_service import ConfirmationService
from services.registration_service import RegistrationService
from dependencies.confirmation import get_confirmation_service
from dependencies.registration import get_registration_service


logger = logging.getLogger(__name__)

users = APIRouter(prefix="/users", tags=["User"])


@users.post("/password-reset-request", status_code=202)
@limiter.limit("1/second")
async def request_password_reset(
    request: Request,
    email: str,
    user_repository: UserRepository = Depends(get_user_repository),
    token_manager: TokenManager = Depends(get_token_manager)
):
    user = await user_repository.get_user_by_email(email)
    if user:
        token_type = "password_reset"
        password_reset_token_lifetime = settings.PASSWORD_RESET_TOKEN_LIFESPAN_MINUTES
        reset_token = await token_manager.create_token(user.id, token_type, expires_delta=password_reset_token_lifetime)
        # Schedule sending the email in the background
        # fdsbackground_tasks.add_task(send_password_reset_email, user.email, reset_token)
        logger.info(
            f"Password reset requested for user {user.id}. Email queued.{reset_token}")

    # Return a generic message regardless of the email's existence in the DB
    return {"message": "If your email is registered with us, you will receive a password reset link shortly."}


@users.post("/password-reset")
async def reset_password(
    token: str,
    new_password: str,
    user_repository: UserRepository = Depends(get_user_repository),
    token_manager: TokenManager = Depends(get_token_manager)
):

    try:
        payload = await token_manager.validate_token(token)
        if "reset_password" not in payload.get("scope", []):
            raise HTTPException(status_code=403, detail="Invalid token")

        user_id = payload['sub']
        await user_repository.update_user_password(int(user_id), new_password)
        await token_manager.invalidate_user_tokens(int(user_id))

        return {"message": "Password successfully reset"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@users.get("/", response_model=List[UserBaseSchema])
@limiter.limit("10/second")
async def get_users(
    request: Request,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    user_repository: UserRepository = Depends(get_user_repository)
):
    logger.info("Grabbing the userstack")
    try:
        users = await user_repository.get_all_users(page=page, page_size=page_size)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed... {e}")


@users.get("/current", response_model=UserBaseSchema)
async def read_users_me(
    current_user: UserModel = Security(
        get_current_active_user, scopes=["users:read"])
):
    return current_user


@users.post("/", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_data: UserCreateSchema,
    user_service: RegistrationService = Depends(get_registration_service)
):
    try:
        return await user_service.register_user(user_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@users.get("/confirm-email")
async def confirm_email(
    token: str,
    confirmation_service: ConfirmationService = Depends(
        get_confirmation_service)
):
    try:
        return await confirmation_service.confirm_email(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
