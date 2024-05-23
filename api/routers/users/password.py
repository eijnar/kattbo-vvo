from fastapi import APIRouter, Depends, status, Request

from utils.rate_limiter import limiter
from services.password_service import PasswordService
from core.dependencies.password_service import get_password_service

router = APIRouter(tags=["password"])

@router.post("/password-reset-request", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
async def request_password_reset(
    request: Request,
    email: str,
    password_service: PasswordService = Depends(get_password_service)
):
    return await password_service.request_password_reset(email)

@router.post("/password-reset", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    token: str,
    new_password: str,
    user_service: PasswordService = Depends(get_password_service)
):
    return await user_service.reset_password(token, new_password)
