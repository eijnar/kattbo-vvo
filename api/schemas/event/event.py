from pydantic import BaseModel, field_serializer, Field, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import date, time

from schemas.event.event_day import EventDayCreate
from schemas.event.event_day import EventDayResponse


class EventBase(BaseModel):
    id: UUID
    name: str
    creator_id: UUID
    event_category_id: UUID
    category: str

    model_config = ConfigDict(from_attributes=True)


class EventResponse(BaseModel):
    id: UUID
    name: str
    creator_id: UUID
    creator_name: str
    event_category_id: UUID
    category: str
    
    model_config = ConfigDict(from_attributes=True)


class EventList(EventBase):
    event: EventBase
    days_count: int


class EventCreateResponse(BaseModel):
    event: EventResponse
    days: List[EventDayResponse]
    
    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    name: str = Field(..., example="Helgjakt")
    event_category_id: UUID = Field(...,
                                    example="123e4567-e89b-12d3-a456-426614174000")
    days: List[EventDayCreate] = Field(..., min_items=1)
    creator_id: UUID = Field(...,
                             example="223e4567-e89b-12d3-a456-426614174001")

    model_config = ConfigDict(from_attributes=True)
