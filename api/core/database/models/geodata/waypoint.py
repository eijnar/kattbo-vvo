import uuid

from sqlalchemy import Column, UUID, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.geodata.waypoint_area import waypoint_areas
from core.database.mixins import TrackingMixin, SoftDeleteMixin

class Waypoint(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'waypoints'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)

    # Relationships
    category = relationship('Category', back_populates='waypoints')
    team = relationship('Team', back_populates='waypoints')
    areas = relationship(
        'Area',
        secondary=waypoint_areas,
        back_populates='waypoints'
    )
    stand_assignments = relationship('WaypointStandAssignment', back_populates='waypoint', cascade="all, delete-orphan")
    tasks = relationship('WaypointTask', back_populates='waypoint', cascade="all, delete-orphan")
