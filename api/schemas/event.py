from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import date, time


class EventBase(BaseModel):
    id: UUID
    name: str
    creator_id: UUID

    model_config = {
        "from_attributes": True
    }


class EventDayBase(BaseModel):
    id: UUID
    date: date
    start_time: time
    end_time: time
    is_cancelled: bool

    model_config = {
        "from_attributes": True
    }


class EventResponse(BaseModel):
    event: EventBase
    days: List[EventDayBase]

    model_config = {
        "from_attributes": True
    }
