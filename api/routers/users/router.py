# routers/users/main.py

from fastapi import APIRouter
from .endpoints import (
    me_api_key,
    me_profile,
    user_management,
    teams
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
    me_profile.router,
    prefix="/me",
    tags=["Profile"]
)

router.include_router(
    me_api_key.router,
    prefix="/me/api-keys",
    tags=["API Keys"]
)

router.include_router(
    teams.router,
    tags=["Team assignments"]
)