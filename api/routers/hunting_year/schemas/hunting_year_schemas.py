from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class HuntingYearCreate(BaseModel):
    start_year: int
    is_current: bool = False
    is_locked: bool = False

class HuntingYearRead(BaseModel):
    id: UUID
    name: str
    start_date: datetime
    end_date: datetime
    is_current: bool
    is_locked: bool

    class Config:
        from_attributes = True