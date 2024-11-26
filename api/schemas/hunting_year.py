from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HuntingYearBase(BaseModel):
    id: UUID
    start_date: datetime
    is_current: bool = False
    is_locked: bool = False

    model_config = {
        "from_attributes": True
    }


class HuntingYearCreate(HuntingYearBase):
    pass


class HuntingYearUpdate(BaseModel):
    is_current: Optional[bool] = Field(
        None, description="Set the hunting year as current")
    is_locked: Optional[bool] = Field(
        None, description="Lock or unlock the hunting year")

    model_config = {
        "from_attributes": True
    }
