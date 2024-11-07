from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from services.hunting_year_service import HuntingYearService
from core.dependencies import get_hunting_year_service
from schemas.hunting_year import HuntingYearCreate, HuntingYearRead, HuntingYearUpdate

router = APIRouter()


@router.post("/", response_model=HuntingYearRead, status_code=status.HTTP_201_CREATED)
async def create_hunting_year(
    hunting_year_data: HuntingYearCreate,
    hunting_year_service: HuntingYearService = Depends(
        get_hunting_year_service)
):
    """
    Create a new hunting year by providing `start_year`. The new hunting year will have corret start and end dates.
    """

    hunting_year = await hunting_year_service.create_hunting_year(
        hunting_year_data
    )

    return hunting_year


@router.get("/", response_model=List[HuntingYearRead])
async def list_hunting_years(
    limit: int = 100,
    offset: int = 0,
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    hunting_years = await service.list_hunting_years(limit=limit, offset=offset)
    return hunting_years


@router.get("/{hunting_year_id}/", response_model=HuntingYearRead)
async def get_hunting_year(
    hunting_year_id: UUID,
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    hunting_year = await service.get_hunting_year(hunting_year_id)
    return hunting_year


@router.patch("/{hunting_year_id}/", response_model=HuntingYearRead)
async def update_hunting_year(
    hunting_year_id: UUID,
    hunting_year_update: HuntingYearUpdate,  # Use the update schema
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    """
    Partially update a hunting year. You can set it as current, lock, or unlock by providing the corresponding fields.
    """
    hunting_year = await service.update_hunting_year(hunting_year_id, hunting_year_update)
    return hunting_year
