import uuid

from sqlalchemy import Index, Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from core.database.base import Base
from core.database.models.geodata.waypoint_area import waypoint_areas
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class Area(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'areas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    
    geometry = Column(
        Geometry(geometry_type='POLYGON', srid=4326),
        nullable=False
    )    
    
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))

    team = relationship('Team', back_populates='areas')
    waypoints = relationship(
        'Waypoint',
        secondary=waypoint_areas,
        back_populates='areas'
    )

    __table_args__ = (
        Index('idx_areas_geometry_v2', 'geometry', postgresql_using='gist'),
    )