from uuid import UUID
from typing import List
from logging import getLogger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.exceptions import DatabaseException
from core.database.models import EventDayGatheringPlace
from repositories.base_repository import BaseRepository


logger = getLogger(__name__)

class EventDayGatheringRepository(BaseRepository[EventDayGatheringPlace]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(EventDayGatheringPlace, db_session)


    async def get_all_by_ids(self, ids: List[UUID]) -> List[EventDayGatheringPlace]:
        try:
            query = select(self.model).where(self.model.id.in_(ids))
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve EventDayGatherings: {e}")
            raise DatabaseException(detail="Failed to retrieve EventDayGatherings.") from e