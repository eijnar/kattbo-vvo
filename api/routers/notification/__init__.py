from fastapi import APIRouter

from .base import router as notification_router

router = APIRouter(tags=["notification"])
router.include_router(notification_router)