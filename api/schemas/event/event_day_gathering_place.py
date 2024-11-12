from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Optional

class EventDayGatheringPlace(BaseModel):
    gathering_place_id: UUID = Field(..., example="323e4567-e89b-12d3-a456-426614174002")
    team_id: Optional[UUID] = Field(None, example="423e4567-e89b-12d3-a456-426614174003")

    model_config = ConfigDict(from_attributes=True)
