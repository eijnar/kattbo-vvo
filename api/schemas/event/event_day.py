from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID
from typing import List
from datetime import date, time

from schemas.event.event_day_gathering_place import EventDayGatheringPlace


class EventDayBase(BaseModel):
    id: UUID
    date: date
    start_time: time
    end_time: time
    cancelled: bool
    event_day_gathering_places: List[EventDayGatheringPlace]

    model_config = ConfigDict(from_attributes=True)


class EventDayResponse(BaseModel):
    id: UUID
    date: date
    start_time: time
    end_time: time
    cancelled: bool
    event_day_gathering_places: List[EventDayGatheringPlace]
    
    model_config = ConfigDict(from_attributes=True)


class EventDayCreate(BaseModel):
    date: date
    start_time: time = Field(..., example="07:00:00")
    end_time: time = Field(..., example="09:00:00")
    event_day_gathering_places: List[EventDayGatheringPlace] = Field(
        ..., min_items=1)

    @field_validator('end_time')
    def end_time_after_start_time(cls, v, info):
        start_time = info.data.get('start_time')
        if start_time and v <= start_time:
            raise ValueError('end_time must be after start_time')
        return v

    model_config = ConfigDict(from_attributes=True)
