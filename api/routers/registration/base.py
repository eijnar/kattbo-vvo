import logging

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from schemas.user import UserCreateSchema
from dependencies.confirmation import get_confirmation_service
from dependencies.registration import get_registration_service
from services.confirmation_service import ConfirmationService
from services.registration_service import RegistrationService

logger = logging.getLogger(__name__)
registration = APIRouter()


@registration.post("/register", status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_data: UserCreateSchema,
    user_service: RegistrationService = Depends(get_registration_service)
):
    try:
        return await user_service.register_user(user_data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@registration.get("/confirm-email")
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
