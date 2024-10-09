from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, Query, Request

from schemas import UserBaseSchema
from services.user_service import UserService
from core.dependencies.user_service import get_user_service
from utils.rate_limiter import limiter



logger = getLogger(__name__)
router = APIRouter(tags=["users"])


@router.get("/", response_model=List[UserBaseSchema])
@limiter.limit("10/second")
async def get_users(
    request: Request,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all_users(page, page_size)
