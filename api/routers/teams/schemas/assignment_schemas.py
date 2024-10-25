from pydantic import BaseModel, Field
from uuid import UUID

class UserTeamAssignmentCreate(BaseModel):
    user_id: UUID
    hunting_year_id: UUID

class UserTeamAssignmentRead(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    hunting_year_id: UUID

    class Config:
        from_attributes = True