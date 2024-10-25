from fastapi import APIRouter
from .endpoints import (
    teams,
    assignments
)

router = APIRouter(
    prefix="/teams",
    tags=["Teams"],
    responses={404: {"description": "Not found"}}
)

# Include sub-routers for different user-related functionalities
router.include_router(teams.router)
router.include_router(assignments.router)