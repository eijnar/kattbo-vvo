from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, status

from core.dependencies import get_event_service
from schemas.event.event import EventCreate, EventCreateResponse, EventDayResponse
from services.event_service import EventService

router = APIRouter()

@router.get("/", response_model=List[EventDayResponse])
async def get_events(
    start: Optional[date] = None,
    end: Optional[date] = None,
    limit: int = 100,
    offset: int = 0, 
    event_service: EventService = Depends(get_event_service)
    ):
    event_days = await event_service.get_all_event_days(limit=limit, offset=offset, start=start, end=end)
    return event_days

@router.get("/{event_id}", response_model=EventCreateResponse)
async def get_event_by_id(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    event, days = await event_service.get_event(event_id)
    return EventCreateResponse(event=event, days=days)

@router.post("/", response_model=EventCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_create: EventCreate,
    event_service: EventService = Depends(get_event_service)
):
    event = await event_service.create_event(event_create)

    return EventCreateResponse(
        event=event,
        days=event.event_days
    )
