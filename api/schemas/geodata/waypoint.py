from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class WaypointBase(BaseModel):
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    category_id: Optional[UUID]
    team_id: Optional[UUID]


class WaypointCreate(WaypointBase):
    name: str = Field(..., example="Sample Waypoint")
    latitude: float = Field(..., example=52.5200)
    longitude: float = Field(..., example=13.4050)
    team_id: UUID


class WaypointUpdate(WaypointBase):
    pass


class WaypointResponse(WaypointBase):
    id: UUID

    model_config={
        "from_attributes": True
    }
