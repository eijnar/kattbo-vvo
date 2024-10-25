import uuid

from sqlalchemy import Column, UUID, String, Date
from sqlalchemy.orm import relationship

from core.database.base import Base


class HuntingYear(Base):
    __tablename__ = 'hunting_years'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date = Column(Date)
    end_date = Column(Date)
    name = Column(String)

    waypoint_stand_assignments = relationship('WaypointStandAssignment', back_populates='hunting_year')
    user_stand_assignments = relationship('UserStandAssignment', back_populates='hunting_year')
    user_team_assignments = relationship('UserTeamAssignment', back_populates='hunting_year')
