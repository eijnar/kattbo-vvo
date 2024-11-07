import uuid

from sqlalchemy import Column, Integer, UUID, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base


class StandNumber(Base):
    __tablename__ = 'stand_numbers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey(
        'teams.id'), nullable=False)
    number = Column(Integer, nullable=False)

    team = relationship('Team', back_populates='stand_numbers')

    __table_args__ = (
        UniqueConstraint('team_id', 'number', name='_team_number_uc'),
    )

    waypoint_stand_assignments = relationship(
        'WaypointStandAssignment', back_populates='stand_number')
    user_stand_assignments = relationship(
        'UserStandAssignment', back_populates='stand_number')
