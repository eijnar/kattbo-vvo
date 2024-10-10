from logging import getLogger

from fastapi import APIRouter, Depends

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
    current_user: UserModel = Depends(get_user_and_check_scopes())
):
    """
    Get the logged in users profile
    """
    logger.debug("Fetching the active user's profile")
    return current_user


@router.put("/", response_model=UserBaseSchema)
async def update_profile(
    user_data: UserUpdateSchema,
    current_user: UserModel = Depends(get_user_and_check_scopes()),
    user_service: UserService = Depends(get_user_service)
):
    
    logger.debug("Starting update of the active user's profile")
    updated_user = await user_service.update_user_profile(current_user, user_data)
    return updated_user
