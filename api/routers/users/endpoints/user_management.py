from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, Query, Request

from core.dependencies import get_user_service
from core.security.dependencies import requires_scope
from utils.rate_limiter import limiter
from routers.users.services.user_service import UserService
from routers.users.schemas.user import UserBaseSchema, UserCreateSchema


logger = getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[UserBaseSchema])
async def get_users(
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    user_service: UserService = Depends(get_user_service)
):
    """
    Retrieve a paginated list of users.
    Accessible to everyone.
    """

    logger.info(f"User requested users list (page: {page}, page_size: {page_size}).")
    return await user_service.get_all_users(page, page_size)


@router.post("/register", dependencies=[Depends(requires_scope("create:user"))])
@limiter.limit("10/second")
async def register_user(
    request: Request,
    user: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
):
    """
    This route is for registering new users, only used by Auth0
    Requires the create:user permission
    """

    logger.debug(f"Received registration request with user data: {user}")
    return await user_service.register_user(user)
