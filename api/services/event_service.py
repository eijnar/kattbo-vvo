from uuid import UUID
from typing import List
from logging import getLogger

from core.exceptions import NotFoundException, ConflictException
from repositories import EventRepository, EventDayRepository
from schemas.event import EventBase, EventResponse


logger = getLogger(__name__)


class EventService:
    def __init__(
        self,
        event_repository = EventRepository,
        event_day_repository = EventDayRepository
    ):
        self.event_repository = event_repository
        self.event_day_repository = event_day_repository
        
    async def get_all_events(self, limit: int = 100, offset: int = 0) -> List[EventBase]:
        events = await self.event_repository.list(limit=limit, offset=offset)
        if not events:
            raise NotFoundException(detail="No events found")
        return events
        
    async def get_event(self, id: str) -> EventResponse:
        event = await self.event_repository.read(id)
        days = await self.event_day_repository.filter(event_id=event.id)
        return event, days
        