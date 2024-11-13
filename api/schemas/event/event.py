from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID
from typing import List, Optional
from datetime import datetime, date

from schemas.event.event_day_gathering_place import EventDayGatheringPlace


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


class EventDayBase(BaseModel):
    id: UUID
    start_datetime: datetime
    end_datetime: datetime
    cancelled: bool

    model_config = ConfigDict(from_attributes=True)


class EventDayResponse(EventDayBase):
    event_day_gathering_places: List[EventDayGatheringPlace]
    event: EventResponse
    
    model_config = ConfigDict(from_attributes=True)


class EventDayCreate(BaseModel):
    start_datetime: datetime = Field(..., example="2024-11-13 09:00:00+01:00")
    end_datetime: datetime = Field(..., example="2024-11-13 12:00:00+01:00")
    event_day_gathering_places: List[EventDayGatheringPlace] = Field(
        ..., min_items=1)

    @field_validator('end_datetime')
    def end_time_after_start_time(cls, v, info):
        start_datetime = info.data.get('start_datetime')
        if start_datetime and v <= start_datetime:
            raise ValueError('end_datetime must be after start_datetime')
        return v

    model_config = ConfigDict(from_attributes=True)


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
