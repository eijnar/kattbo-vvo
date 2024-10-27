# dependencies/hunting_year_dependency.py

from logging import getLogger
from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from services.hunting_year_service import HuntingYearService
from core.dependencies import get_hunting_year_service
from core.database.models import HuntingYear
from core.exceptions import NotFoundException


logger = getLogger(__name__)

async def get_resolved_hunting_year(
    hunting_year_id: Optional[UUID] = None,
    hunting_year_service: HuntingYearService = Depends(get_hunting_year_service),
) -> HuntingYear:
    """
    Resolves the hunting year based on the provided ID.
    If no ID is provided, returns the current hunting year.
    """
    try:
        hunting_year = await hunting_year_service.resolve_hunting_year(hunting_year_id)
        return hunting_year
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        ) from e
    except Exception as e:
        # Handle other potential exceptions
        logger.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while resolving the hunting year."
        ) from e
