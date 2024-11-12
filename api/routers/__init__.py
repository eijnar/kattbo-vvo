from fastapi import APIRouter

from routers.users.router import router as users_router
from routers.team.router import router as teams_router
from routers.hunting_year.router import router as hunting_years_router
from routers.event.router import router as event_router
from routers.waypoint.router import router as waypoint_router

api_router = APIRouter()

# Include all module routers with their respective prefixes
api_router.include_router(users_router)
api_router.include_router(teams_router)
api_router.include_router(hunting_years_router)
api_router.include_router(event_router)
api_router.include_router(waypoint_router)
