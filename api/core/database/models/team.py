import uuid

from sqlalchemy import Column, UUID, String, Boolean
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, SoftDeleteMixin

class Team(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'teams'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    
    user_team_assignments = relationship('UserTeamAssignment', back_populates='team', cascade="all, delete-orphan") 
    areas = relationship('Area', back_populates='team')
    waypoints = relationship('Waypoint', back_populates='team')
    stand_numbers = relationship('StandNumber', back_populates='team')