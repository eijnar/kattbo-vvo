from fastapi import APIRouter

from .users import router as users_router
from .notification import router as notification_router

router = APIRouter()
router.include_router(users_router)
router.include_router(notification_router)