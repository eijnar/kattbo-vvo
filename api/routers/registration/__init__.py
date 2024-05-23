from fastapi import APIRouter

from .base import router as registration_router

router = APIRouter(tags=["registration"])
router.include_router(registration_router)