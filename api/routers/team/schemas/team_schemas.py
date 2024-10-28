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

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class AreaRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class WaypointRead(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class StandNumberRead(BaseModel):
    id: UUID
    number: int

    class Config:
        from_attributes = True

class TeamRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True