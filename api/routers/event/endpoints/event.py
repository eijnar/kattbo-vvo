from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from core.dependencies import get_event_service
from schemas.event.event import EventBase, EventResponse, EventCreate, EventCreateResponse
from services.event_service import EventService

router = APIRouter()

@router.get("/", response_model=List[EventBase])
async def get_events(limit: int = 100, offset: int = 0, event_service: EventService = Depends(get_event_service)):
    events = await event_service.get_all_events(limit=limit, offset=offset)
    return events

@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: UUID, event_service: EventService = Depends(get_event_service)):
    event, days = await event_service.get_event(event_id)
    return EventResponse(event=event, days=days)

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
