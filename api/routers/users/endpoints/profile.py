from logging import getLogger

from fastapi import APIRouter, Depends, Request

from core.database.models import UserModel
from core.security.dependencies import get_user_and_check_scopes
from core.dependencies import get_user_service
from ..schemas.user import UserBaseSchema, UserUpdateSchema
from routers.users.services.user_service import UserService
from utils.rate_limiter import limiter


logger = getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=UserBaseSchema)
async def get_self_profile(
    request: Request,
    current_user: UserModel = Depends(get_user_and_check_scopes())
):
    """
    Get the logged in users profile
    """
    logger.info(
        "Fetching user's profile",
        extra={
            "user.id": str(current_user.id),
            **request.state.http_request,  # Include request info
        })
    return current_user


@router.put("/", response_model=UserBaseSchema)
async def update_profile(
    request: Request,
    user_data: UserUpdateSchema,
    current_user: UserModel = Depends(get_user_and_check_scopes()),
    user_service: UserService = Depends(get_user_service)
):

    logger.info(
        "Starting update user's profile",
        extra={
            "user.id": str(current_user.id),
            **request.state.http_request,  # Include request info
        })
    updated_user = await user_service.update_user_profile(current_user, user_data)
    return updated_user


@router.patch("/", response_model=UserBaseSchema)
async def partial_update_profile(
    request: Request,
    user_data: UserUpdateSchema,
    current_user: UserModel = Depends(get_user_and_check_scopes()),
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
