from fastapi import APIRouter

from .token import router as token_router
from .login import router as login_router
from .authorize import router as auth_router

router = APIRouter(tags=["OAuth2"])
router.include_router(token_router)
router.include_router(login_router)
router.include_router(auth_router)