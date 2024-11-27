from uuid import uuid4

from sqlalchemy import Column, ForeignKey, UUID, Boolean, CheckConstraint
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin


class EventDayGatheringPlace(Base, TrackingMixin):
    __tablename__ = 'event_day_gathering_places'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    is_joint = Column(Boolean, nullable=False, default=False)

    event_day_id = Column(UUID(as_uuid=True), ForeignKey('event_days.id', ondelete='CASCADE'))
    gathering_place_id = Column(UUID(as_uuid=True), ForeignKey('waypoints.id'))
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))

    event_day = relationship('EventDay', back_populates='event_day_gathering_places', lazy='selectin')
    gathering_place = relationship('Waypoint', back_populates='event_day_gathering_places', lazy='selectin')
    team = relationship('Team', back_populates='event_day_gathering_places', lazy='selectin')

    __table_args__ = (
        CheckConstraint(
            "(is_joint = TRUE AND team_id IS NULL) OR (is_joint = FALSE AND team_id IS NOT NULL)",
            name='chk_is_joint_team_id'
        ),
    )
