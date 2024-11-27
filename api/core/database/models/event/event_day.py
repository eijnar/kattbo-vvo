from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class EventDay(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'event_days'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    start_datetime = Column(DateTime(timezone=True), nullable=True)
    end_datetime = Column(DateTime(timezone=True), nullable=True)
    cancelled = Column(Boolean, default=False)
    sequence = Column(Integer, default=1)

    # Relationships
    event_id = Column(UUID(as_uuid=True), ForeignKey(
        'events.id', ondelete='CASCADE'), nullable=False)

    event = relationship('Event', back_populates='event_days', lazy='selectin')
    user_events = relationship(
        'UserEventRegistration', back_populates='event_day', lazy='selectin')

    event_day_gathering_places = relationship(
        'EventDayGatheringPlace', back_populates='event_day', lazy='selectin', cascade='all, delete-orphan')

    @hybrid_property
    def registration_count(self):
        return len(self.user_events)

    @registration_count.expression
    def registration_count(cls):
        return (
            select(func.count('UserEventRegistration.id'))
            .where('UserEventRegistration.event_day_id' == cls.id)
            .correlate(cls)
            .scalar_subquery()
        )