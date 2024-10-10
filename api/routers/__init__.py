from fastapi import APIRouter
from .users.main import router as users_router

api_router = APIRouter()

# Include all module routers with their respective prefixes
api_router.include_router(users_router)
