# routers/users/main.py

from fastapi import APIRouter
from .endpoints import (
    user_management,
    profile
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

# Include sub-routers for different user-related functionalities
router.include_router(
    user_management.router,
    tags=["User Management"]
)

router.include_router(
    profile.router,
    prefix="/profile",
    tags=["Profile"]
)