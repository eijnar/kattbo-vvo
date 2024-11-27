from pydantic import BaseModel, Field, ConfigDict, computed_field
from uuid import UUID
from typing import Optional, Any


class EventDayGatheringPlace(BaseModel):
    team_id: Optional[UUID] = Field(
        None, example="423e4567-e89b-12d3-a456-426614174003")
    is_joint: bool

    model_config = ConfigDict(from_attributes=True)

    gathering_place: Any = Field(exclude=True)

    @computed_field
    @property
    def id(self) -> UUID:
        return self.gathering_place.id

    @computed_field
    @property
    def name(self) -> UUID:
        return self.gathering_place.name

    @computed_field
    @property
    def longitude(self) -> float:
        return self.gathering_place.longitude

    @computed_field
    @property
    def latitude(self) -> float:
        return self.gathering_place.latitude
