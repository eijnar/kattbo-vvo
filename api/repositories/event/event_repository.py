from logging import getLogger
from typing import List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlalchemy.future import select
from sqlalchemy import and_, exists

from core.exceptions import DatabaseError, NotFoundError
from repositories.base_repository import BaseRepository
from core.database.models import Event, EventDay


logger = getLogger(__name__)


class EventRepository(BaseRepository[Event]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(Event, db_session)

    async def create_event(self, event_data: Event) -> Event:
        try:
            self.db_session.add(event_data)
            await self.db_session.flush()
            await self.db_session.commit()

            query = select(Event).options(
                selectinload(Event.event_days).selectinload(
                    EventDay.event_day_gathering_places)
            ).where(Event.id == event_data.id)
            result = await self.db_session.execute(query)
            event = result.scalar_one()

            logger.debug(f"Event fetched with relationships: {event}")

            return event

        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(
                f"Failed to create event and days: {e}", exc_info=True)
            raise DatabaseError(
                detail="Failed to create event and associated days.") from e

    async def list_events_with_days_by_date_range(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        raise_if_not_found: bool = False
    ) -> List[Event]:
        try:
            logger.info(
                "Listing Events with EventDays",
                extra={
                    "limit": limit,
                    "offset": offset,
                    "start": start,
                    "end": end
                }
            )

            query = select(Event).options(with_loader_criteria(
                EventDay, EventDay.is_active == True)).where(Event.is_active == True)

            event_day_conditions = [EventDay.is_active == True]
            if start:
                event_day_conditions.append(EventDay.start_datetime >= start)
            if end:
                event_day_conditions.append(EventDay.end_datetime <= end)

            # Update the exists clause to include date filters
            query = query.where(
                exists(
                    select(EventDay.id).where(
                        EventDay.event_id == Event.id,
                        and_(*event_day_conditions)
                    )
                )
            )

            query = query.limit(limit).offset(offset)

            result = await self.db_session.execute(query)
            events = result.scalars().unique().all()

            if not events and raise_if_not_found:
                logger.info("No Event records found", extra={"count": 0})
                raise NotFoundError(detail="No records found")

            logger.info(f"Listed {len(events)} Event(s)",
                        extra={"count": len(events)})
            return events

        except SQLAlchemyError as e:
            logger.error(f"Failed to list Events with EventDays: {e}")
            raise DatabaseError(
                detail="Failed to list Events with EventDays."
            ) from e
