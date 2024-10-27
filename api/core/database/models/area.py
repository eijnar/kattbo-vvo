import uuid

from sqlalchemy import Column, Integer, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.waypoint_area import waypoint_areas


class Area(Base):
    __tablename__ = 'areas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))

    team = relationship('Team', back_populates='areas')
    waypoints = relationship(
        'Waypoint',
        secondary=waypoint_areas,
        back_populates='areas'
    )