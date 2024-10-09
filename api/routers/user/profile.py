from logging import getLogger

from fastapi import APIRouter, Depends

from schemas import UserBaseSchema, UserUpdateSchema
from services.user_service import UserService
from core.database.models import UserModel
from utils.rate_limiter import limiter
from core.security.dependencies import get_user_and_check_scopes
from core.dependencies.user_service import get_user_service


logger = getLogger(__name__)
router = APIRouter(tags=["user"])


@router.get("/", response_model=UserBaseSchema)
async def get_self_profile(
    current_user: UserModel = Depends(get_user_and_check_scopes())
):
    return current_user


@router.put("/", response_model=UserBaseSchema)
async def update_profile(
    user_data: UserUpdateSchema,
    current_user: UserModel = Depends(get_user_and_check_scopes()),
    user_service: UserService = Depends(get_user_service)
):
    logger.info("Trying to update user")
    updated_user = await user_service.update_user_profile(current_user, user_data)
    return updated_user
