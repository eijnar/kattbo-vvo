from logging import getLogger

from fastapi import APIRouter, Depends, Request

from core.database.models import User
from core.security.auth import get_current_active_user
from core.security.models import UserContext
from core.dependencies import get_user_service
from schemas import UserBase, UserUpdate
from services.user_service import UserService


logger = getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=UserBase)
async def get_self_profile(
    request: Request,
    user_context: UserContext = Depends(
        get_current_active_user()),
):
    """
    Get the logged in users profile
    """
    current_user = user_context.user
    logger.info(
        "Fetching user's profile",
        extra={
            "user.id": str(current_user.id),
            **request.state.http_request,  # Include request info
        })
    return current_user


@router.put("/", response_model=UserBase)
async def update_profile(
    request: Request,
    user_data: UserUpdate,
    user_context: UserContext = Depends(get_current_active_user()),
    user_service: UserService = Depends(get_user_service)
):
    current_user = user_context.user

    logger.info(
        "Starting update user's profile",
        extra={
            "user.id": str(current_user.id),
            **request.state.http_request,  # Include request info
        })
    updated_user = await user_service.update_user_profile(current_user, user_data)
    return updated_user


@router.patch("/", response_model=UserBase)
async def partial_update_profile(
    request: Request,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    logger.info(
        "Starting partial update of user's profile",
        extra={
            "user.id": str(current_user.id),
            **request.state.http_request,
        })

    updated_user = await user_service.update_user_profile_partial(current_user, user_data)
    return updated_user
