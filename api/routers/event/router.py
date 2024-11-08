from fastapi import APIRouter

from .endpoints import (
    event
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


router.include_router(event.router)