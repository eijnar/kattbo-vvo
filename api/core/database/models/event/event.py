from uuid import uuid4

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class Event(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String, unique=True)
    
    # Relationships
    
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    # event_type_id = Column(UUID(as_uuid=True), ForeignKey('event_types.id'), nullable=False)
    
    event_category = relationship("EventCategory", back_populates="events")
    event_days = relationship("EventDay", back_populates="events", cascade="all,delete")