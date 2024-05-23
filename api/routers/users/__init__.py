from fastapi import APIRouter
from .base import router as user_router
from .password import router as password_router

router = APIRouter(tags=["users"])
router.include_router(user_router, prefix="/users")
router.include_router(password_router)