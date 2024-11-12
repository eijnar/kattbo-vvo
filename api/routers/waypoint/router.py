from fastapi import APIRouter
from .endpoints import (
    waypoints
)

router = APIRouter(
    prefix="/waypoints",
    tags=["Waypoints"],
    responses={404: {"description": "Not found"}}
)

# Include sub-routers for different user-related functionalities
router.include_router(waypoints.router)
