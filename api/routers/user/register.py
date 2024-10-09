from logging import getLogger

from fastapi import APIRouter, Depends, Request

from schemas import UserCreateSchema
from services.user_service import UserService
from core.security.dependencies import requires_scope
from core.dependencies.user_service import get_user_service

logger = getLogger(__name__)

router = APIRouter(tags=["user"])


@router.post("/register", dependencies=[Depends(requires_scope("create:user"))])
async def register_user(
    request: Request,
    user: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
):
    logger.info(f"Received registration request with user data: {user}")
    return await user_service.register_user(user)
