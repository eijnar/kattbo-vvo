from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID

class HuntYearCreate(BaseModel):
    year: str = Field(..., description="The start of the new hunt year...")

class HuntYearRead(BaseModel):
    id: UUID
    year: str
    is_current: bool
    is_locked: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserTeamYearCreate(BaseModel):
    user_id: UUID
    hunt_year_id: UUID
    hunt_team_id: UUID