from pydantic import BaseModel, Field, UUID4
from typing import Optional, List
from datetime import datetime

from schemas.hunting_year import HuntingYearRead
from routers.team.schemas.team_schemas import UserRead

class UserTeamAssignmentCreate(BaseModel):
    team_id: UUID4 = Field(..., description="The UUID of the user to assign.")
    hunting_year_id: Optional[UUID4] = Field(
        None, description="The UUID of the hunting year. Defaults to the current hunting year if not provided."
    )

# schemas/user_team_assignment.py

class UserTeamAssignmentRead(BaseModel):
    id: UUID4
    user_id: UUID4
    team_id: UUID4
    hunting_year_id: Optional[UUID4]
    assigned_at: datetime

    model_config = {
        "from_attributes": True
    }


class TeamUsersResponse(BaseModel):
    hunting_year: HuntingYearRead
    users: List[UserRead]
    
    model_config = {
        "from_attributes": True
    }