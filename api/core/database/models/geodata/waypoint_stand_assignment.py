import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database.base import Base


class WaypointStandAssignment(Base):
    __tablename__ = 'waypoint_stand_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    waypoint_id = Column(UUID(as_uuid=True), ForeignKey('waypoints.id'))
    area_id = Column(UUID(as_uuid=True), ForeignKey('areas.id'))
    stand_number_id = Column(
        UUID(as_uuid=True), ForeignKey('stand_numbers.id'))
    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))

    waypoint = relationship('Waypoint', back_populates='stand_assignments')
    area = relationship('Area')
    stand_number = relationship(
        'StandNumber', back_populates='waypoint_stand_assignments')
    hunting_year = relationship(
        'HuntingYear', back_populates='waypoint_stand_assignments')

    __table_args__ = (
        UniqueConstraint('waypoint_id', 'area_id',
                         'hunting_year_id', name='_waypoint_area_hyear_uc'),
    )
