from uuid import uuid4

from sqlalchemy import Column, UUID, ForeignKey, String
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class EventCategory(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'event_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    
    events = relationship('Event', backref='event_category', lazy=True)
    