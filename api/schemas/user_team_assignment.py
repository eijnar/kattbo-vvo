from pydantic import BaseModel
from uuid import UUID


class UserTeamAssignmentRead(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    hunting_year_id: UUID
    
    model_config = {
        "from_attributes": True
    }