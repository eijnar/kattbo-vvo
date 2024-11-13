from logging import getLogger
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from core.exceptions import DatabaseException
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
                selectinload(Event.event_days).selectinload(EventDay.event_day_gathering_places)
            ).where(Event.id == event_data.id)
            result = await self.db_session.execute(query)
            event = result.scalar_one()

            logger.debug(f"Event fetched with relationships: {event}")

            return event
        
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            logger.error(f"Failed to create event and days: {e}", exc_info=True)
            raise DatabaseException(detail="Failed to create event and associated days.") from e