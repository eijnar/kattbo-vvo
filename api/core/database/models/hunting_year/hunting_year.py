import uuid

from sqlalchemy import Column, UUID, String, DateTime, Boolean
from sqlalchemy.orm import relationship, validates

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin, LockableMixin


class HuntingYear(Base, TrackingMixin, SoftDeleteMixin, LockableMixin):
    __tablename__ = 'hunting_years'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    is_current = Column(Boolean, default=False, nullable=False)

    waypoint_stand_assignments = relationship(
        'WaypointStandAssignment', back_populates='hunting_year')

    user_stand_assignments = relationship(
        'UserStandAssignment', back_populates='hunting_year')

    user_team_assignments = relationship(
        'UserTeamAssignment', back_populates='hunting_year')

    hunting_year_tasks = relationship(
        'HuntingYearTask', back_populates='hunting_year', cascade="all, delete-orphan")

    user_assignments = relationship(
        'UserHuntingYearAssignment',
        back_populates='hunting_year',
        cascade="all, delete-orphan"
    )

    licenses = relationship(
        'HuntingYearLicense',
        back_populates='hunting_year',
        cascade="all, delete-orphan"
    )

    @validates('name')
    def validate_name(self, key, name):
        import re
        pattern = r'^(\d{4})/(\d{4})$'  # YYYY/YYYY
        match = re.match(pattern, name)
        if not match:
            raise ValueError("Name must be in the format YYYY/YYYY")

        start_year, end_year = map(int, match.groups())
        if end_year != start_year + 1:
            raise ValueError(
                "The second year must be exactly one greater than the first year")

        return name
