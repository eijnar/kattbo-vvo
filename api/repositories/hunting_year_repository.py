from uuid import UUID
from logging import getLogger
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from core.database.models import HuntingYear
from core.exceptions import DatabaseException, NotFoundException
from repositories.base_repository import BaseRepository


logger = getLogger(__name__)


class HuntingYearRepository(BaseRepository[HuntingYear]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(HuntingYear, db_session)

    async def get_current_hunting_year(self) -> Optional[HuntingYear]:
        """Retrieve the HuntingYear marked as current"""
        logger.debug("Retrieving the current hunting year", extra={"resource.type": "HuntingYear"})
        return await self.read(is_current=True, raise_if_not_found=False)

    async def get_by_name(self, name: str) -> Optional[HuntingYear]:
        return await self.read(name=name)

    async def list_hunting_years_descending(self, limit: int = 100, offset: int = 0) -> List[HuntingYear]:
        """List HuntingYears ordered by start_date descending"""
        try:
            query = select(self.model).order_by(
                self.model.start_date.desc()).limit(limit).offset(offset)
            result = await self.db_session.execute(query)
            hunting_years = result.scalars().all()
            return hunting_years
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Failed to list HuntingYears"
            )
