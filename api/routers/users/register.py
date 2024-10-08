import logging

from fastapi import APIRouter, Depends

from schemas import UserCreateSchema
from services.user_service import UserService
from core.security.dependencies import requires_scope
from core.dependencies.user_service import get_user_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["user"])


@router.post("/register", dependencies=[Depends(requires_scope("create:user"))])
async def register_user(
    user: UserCreateSchema,
    user_service: UserService = Depends(get_user_service)
):
    logging.info(f"Received registration request with user data: {user}")
    return await user_service.register_user(user)
