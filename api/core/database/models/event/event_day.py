from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Date, Time, Boolean
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class EventDay(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'event_days'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date = Column(Date, nullable=False)
    start_time = Column(Time(timezone=True), default='07:00:00', nullable=True)
    end_time = Column(Time(timezone=True), default='16:00:00', nullable=True)
    cancelled = Column(Boolean, default=False)
    sequence = Column(Integer, default=0)
    
    # Relationships
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    
    events = relationship('Event', back_populates='event_days')
    user_events = relationship('UserEventRegistration', back_populates='event_day')
    
    event_day_gathering_places = relationship('EventDayGatheringPlace', back_populates='event_day', lazy='selectin', cascade='all, delete-orphan')