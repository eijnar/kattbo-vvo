from fastapi import APIRouter
from .base import router as user_router
from .register import router as register_router


router = APIRouter(tags=["users"])
router.include_router(user_router, prefix="/users")
router.include_router(register_router)
