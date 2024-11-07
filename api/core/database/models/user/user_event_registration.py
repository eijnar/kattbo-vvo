from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import Column, UUID, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin


class UserEventRegistration(Base, TrackingMixin):
    __tablename__ = 'user_event_registrations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    half_day = Column(Boolean, default=False)
    registered_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # Relationships
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    event_day_id = Column(UUID(as_uuid=True), ForeignKey('event_days.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship('User', back_populates='user_events')
    days = relationship('EventDay', back_populates='user_events')