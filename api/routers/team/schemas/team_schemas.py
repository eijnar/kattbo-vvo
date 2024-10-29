from pydantic import BaseModel
from uuid import UUID

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }

class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    
    model_config = {
        "from_attributes": True
    }

class AreaRead(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }

class WaypointRead(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float

    model_config = {
        "from_attributes": True
    }

class StandNumberRead(BaseModel):
    id: UUID
    number: int

    model_config = {
        "from_attributes": True
    }

class TeamRead(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }