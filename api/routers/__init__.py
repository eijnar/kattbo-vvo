from fastapi import APIRouter
from .users.router import router as users_router
from .team.router import router as teams_router
from routers.hunting_year.router import router as hunting_years_router

api_router = APIRouter()

# Include all module routers with their respective prefixes
api_router.include_router(users_router)
api_router.include_router(teams_router)
api_router.include_router(hunting_years_router)
