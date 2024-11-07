from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HuntingYearBase(BaseModel):
    start_year: int
    is_current: bool = False
    is_locked: bool = False

    model_config = {
        "from_attributes": True
    }


class HuntingYearCreate(HuntingYearBase):
    pass


class HuntingYearUpdate(BaseModel):
    is_current: Optional[bool] = Field(None, description="Set the hunting year as current")
    is_locked: Optional[bool] = Field(None, description="Lock or unlock the hunting year")

    model_config = {
        "from_attributes": True
    }


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
