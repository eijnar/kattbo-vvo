from fastapi import APIRouter
from .profile import router as user_router
from .register import router as register_router


router = APIRouter(tags=["user"])
router.include_router(user_router, prefix="/user")
router.include_router(register_router)