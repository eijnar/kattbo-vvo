from fastapi import APIRouter
from .endpoints import (
    hunting_years
)

router = APIRouter(
    prefix="/hunting_years",
    tags=["Hunting years"],
    responses={404: {"description": "Not found"}}
)

router.include_router(hunting_years.router)