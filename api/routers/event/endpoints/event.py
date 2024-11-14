from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from logging import getLogger

from fastapi import APIRouter, Depends, status, Response
from icalendar import Calendar, Event as ICalEvent, vCalAddress, vText, vGeo, vRecur
from shapely.geometry import Point

from core.dependencies import get_event_service
from schemas.event.event import EventCreate, EventCreateResponse, EventDayResponse
from services.event_service import EventService
from utils.generate_ical import generate_ical

logger = getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[EventDayResponse])
async def get_events_json(
    start: Optional[date] = None,
    end: Optional[date] = None,
    limit: int = 100,
    offset: int = 0,
    event_service: EventService = Depends(get_event_service)
):
    """
    This route will list events for FullCalendar required JSON format
    """
    
    event_days = await event_service.get_all_event_days(limit=limit, offset=offset, start=start, end=end)
    return event_days


@router.get("/ical")
async def generate_ical_route(
    user_id: UUID,
    event_service: EventService = Depends(get_event_service)
):
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
