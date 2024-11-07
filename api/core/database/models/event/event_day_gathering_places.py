from uuid import uuid4

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin


class EventDayGatheringPlaces(Base, TrackingMixin):
    __tablename__ = 'event_day_gathering_places'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())

    event_day_id = Column(UUID(as_uuid=True), ForeignKey('event_days.id'))
    gathering_place_id = Column(UUID(as_uuid=True), ForeignKey('waypoints.id'))
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))
    
    event_day = relationship('EventDay', backref=(
        'event_day_gathering_places'), lazy='selectin', cascade='all, delete-orphan')
    gathering_place = relationship('Waypoint', backref=(
        'event_day_gathering_places'), lazy='selectin', cascade='all, delete-orphan')
    team = relationship('Team', backref=(
        'event_day_gathering_places'), lazy='selectin', cascade='all, delete-orphan')
