# schemas/team.py
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
from schemas.common import UserRead, HuntingYearRead, WaypointRead


class TeamBase(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass



class TeamUsersResponse(BaseModel):
    hunting_year: HuntingYearRead
    users: List[UserRead]

    model_config = {
        "from_attributes": True
    }
