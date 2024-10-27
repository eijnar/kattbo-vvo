from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserTeamAssignmentCreate(BaseModel):
    user_id: UUID = Field(..., description="The UUID of the user to assign.")
    hunting_year_id: Optional[UUID] = Field(
        None, description="The UUID of the hunting year. Defaults to the current hunting year if not provided."
    )

# schemas/user_team_assignment.py

class UserTeamAssignmentRead(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    hunting_year_id: UUID
    assigned_at: datetime

    class Config:
        orm_mode = True
