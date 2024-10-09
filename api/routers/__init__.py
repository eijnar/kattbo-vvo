from fastapi import APIRouter

from .user import router as user_router
from .users import router as users_router
from .notification import router as notification_router

router = APIRouter()
router.include_router(user_router)
router.include_router(users_router)
router.include_router(notification_router)