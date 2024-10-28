# routers/hunting_year/endpoints/hunting_years.py

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from services.hunting_year_service import HuntingYearService
from core.dependencies import get_hunting_year_service
from core.exceptions import ConflictException, ValidationException, DatabaseException, NotFoundException
from routers.hunting_year.schemas.hunting_year_schemas import HuntingYearCreate, HuntingYearRead

router = APIRouter()

@router.post("/", response_model=HuntingYearRead, status_code=status.HTTP_201_CREATED)
async def create_hunting_year(
    hunting_year_data: HuntingYearCreate,
    hunting_year_service: HuntingYearService = Depends(get_hunting_year_service)
):
    try:
        hunting_year = await hunting_year_service.create_hunting_year(
            hunting_year_data
        )
        return hunting_year
    except ConflictException as ce:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ce.detail) from ce
    except ValidationException as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ve.detail) from ve
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de.detail) from de

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
    try:
        hunting_year = await service.get_hunting_year(hunting_year_id)
        return hunting_year
    except NotFoundException as nfe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=nfe.detail)

@router.put("/{hunting_year_id}/set-current/", response_model=HuntingYearRead)
async def set_current_hunting_year(
    hunting_year_id: UUID,
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    try:
        hunting_year = await service.set_current_hunting_year(hunting_year_id)
        return hunting_year
    except NotFoundException as nfe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=nfe.detail)
    except ConflictException as ce:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ce.detail)
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de.detail)

@router.put("/{hunting_year_id}/lock/", response_model=HuntingYearRead)
async def lock_hunting_year(
    hunting_year_id: UUID,
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    try:
        hunting_year = await service.lock_hunting_year(hunting_year_id)
        return hunting_year
    except NotFoundException as nfe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=nfe.detail)
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de.detail)

@router.put("/{hunting_year_id}/unlock/", response_model=HuntingYearRead)
async def unlock_hunting_year(
    hunting_year_id: UUID,
    service: HuntingYearService = Depends(get_hunting_year_service)
):
    try:
        hunting_year = await service.unlock_hunting_year(hunting_year_id)
        return hunting_year
    except NotFoundException as nfe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=nfe.detail)
    except DatabaseException as de:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=de.detail)
