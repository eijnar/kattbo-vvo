from uuid import UUID
from typing import Optional

from core.database.models import HuntingYear
from core.exceptions import NotFoundError


class BaseService:
    def __init__(self, hunting_year_service):
        self.hunting_year_service = hunting_year_service
        
    async def resolve_hunting_year(self, hunting_year_id: Optional[UUID] = None) -> HuntingYear:
        if hunting_year_id:
            hunting_year = await self.hunting_year_service.get_hunting_year(hunting_year_id)
            if not hunting_year:
                raise NotFoundError(detail=f"HuntingYear with ID {hunting_year_id} not found.")
            return hunting_year
        else:
            hunting_year = await self.hunting_year_service.get_current_hunting_year()
            if not hunting_year:
                raise NotFoundError(detail="No current HuntingYear is set.")
            return hunting_year