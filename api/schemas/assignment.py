from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime


class UserTeamAssignmentCreate(BaseModel):
    user_id: UUID4 = Field(..., description="The UUID of the user to assign")
    team_id: UUID4 = Field(..., description="The UUID of the team to assign the user to.")
    hunting_year_id: Optional[UUID4] = Field(
        None, description="The UUID of the hunting year. Defaults to the current hunting year if not provided."
    )


class UserTeamAssignmentRead(BaseModel):
    id: UUID4
    user_id: UUID4
    team_id: UUID4
    hunting_year_id: Optional[UUID4]
    assigned_at: datetime

    model_config = {
        "from_attributes": True
    }
