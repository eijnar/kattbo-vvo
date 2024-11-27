from typing import List, Optional
from datetime import datetime
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from core.exceptions import DatabaseError, NotFoundError
from repositories.base_repository import BaseRepository
from core.database.models import EventDay


logger = getLogger(__name__)


class EventDayRepository(BaseRepository[EventDay]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(EventDay, db_session)

    async def list_by_date_range(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        raise_if_not_found: bool = False
    ) -> List[EventDay]:
        try:
            logger.info(
                "Listing EventDays",
                extra={
                    "limit": limit,
                    "offset": offset,
                    "start": start,
                    "end": end
                }
            )
            query = select(EventDay).where(EventDay.is_active == True)

            if start:
                query = query.where(EventDay.start_datetime >= start)
            if end:
                query = query.where(EventDay.end_datetime <= end)

            query = query.limit(limit).offset(offset)

            result = await self.db_session.execute(query)
            records = result.scalars().all()
            if records:
                logger.info(
                    f"Listed {len(records)} EventDay(s)",
                    extra={"count": len(records)}
                )
            else:
                logger.info(
                    "No EventDay records found",
                    extra={"count": 0}
                )
                if raise_if_not_found:
                    raise NotFoundError(detail="No records found")

            return records

        except SQLAlchemyError as e:
            logger.error(f"Failed to list EventDays: {e}")
            raise DatabaseError(
                detail="Failed to list EventDays."
            ) from e

