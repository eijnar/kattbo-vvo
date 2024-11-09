from pydantic import BaseModel, field_serializer
from uuid import UUID
from typing import List
from datetime import date, time


class EventBase(BaseModel):
    id: UUID
    name: str
    creator_id: UUID
    creator_name: str

    category: str

    model_config = {
        "from_attributes": True
    }


class EventList(EventBase):
    events: EventBase


class EventDayBase(BaseModel):
    id: UUID
    date: date
    start_time: time
    end_time: time
    cancelled: bool

    model_config = {
        "from_attributes": True
    }


class EventResponse(BaseModel):
    event: EventBase
    days: List[EventDayBase]

    model_config = {
        "from_attributes": True
    }
