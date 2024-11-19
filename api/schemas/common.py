# schemas/common.py
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class UserRead(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }


class AreaRead(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }


class WaypointRead(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float

    model_config = {
        "from_attributes": True
    }


class TeamRead(BaseModel):
    id: UUID
    name: str


class HuntingYearRead(BaseModel):
    id: UUID
    name: str
    start_date: datetime
    end_date: datetime
    is_current: bool
    is_locked: bool

    model_config = {
        "from_attributes": True
    }


class StandNumberRead(BaseModel):
    id: UUID
    number: int

    model_config = {
        "from_attributes": True
    }
