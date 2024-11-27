from typing import List, Optional, Literal, Union
from uuid import UUID
from datetime import date
from logging import getLogger

from fastapi import APIRouter, Depends, status, Response, Request

from core.dependencies import get_event_service
from schemas.event.event import EventCreate, EventCreateResponse, EventDayResponse, GroupedEventResponse
from services.event_service import EventService
from utils.generate_ical import generate_ical

logger = getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=Union[List[GroupedEventResponse], List[EventDayResponse]])
async def get_events_json(
    start: Optional[date] = None,
    end: Optional[date] = None,
    limit: int = 100,
    offset: int = 0,
    event_service: EventService = Depends(get_event_service),
    format: Literal["flattened", "grouped"] = "grouped"
):
    """
    This route will list events for FullCalendar required JSON format
    """
    
    if format == 'grouped':
        events = await event_service.get_all_events_with_days(limit=limit, offset=offset, start=start, end=end)
        logger.debug(f"grouped: {events}")
        return events
    
    elif format == 'flattened':
        event_days = await event_service.get_all_event_days(limit=limit, offset=offset, start=start, end=end)
        logger.debug(f"flattened: {event_days}")
        return event_days
    
    


@router.get("/ical.ics")
async def generate_ical_route(
    request: Request,
    user_id: UUID,
    event_service: EventService = Depends(get_event_service)
):
    
    logger.info(f"Request URL: {request.url}")
    logger.info(f"Headers: {request.headers}")
    events = await event_service.get_all_event_days(limit=None, offset=None)
    ical_data = await generate_ical(events)

    response = Response(content=ical_data, media_type='text/calendar; charset=utf-8')
    response.headers['Content-Disposition'] = 'attachment; filename="kattbo_vvo.ics"'
    return response
            

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
