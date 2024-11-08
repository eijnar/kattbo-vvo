from typing import List

from fastapi import APIRouter, Depends

from core.dependencies import get_event_service
from schemas.event import EventBase
from services.event_service import EventService

router = APIRouter()

@router.get("/", response_model=List[EventBase])
async def get_events(limit: int = 100, offset: int = 0, event_service: EventService = Depends(get_event_service)):
    events = await event_service.get_all_events(limit=limit, offset=offset)
    return events