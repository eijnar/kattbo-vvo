from uuid import uuid4

from sqlalchemy import Column, UUID, String, ForeignKey, desc, asc
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin
from core.database.models.event.event_day import EventDay


class Event(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'events'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    event_category_id = Column(UUID(as_uuid=True), ForeignKey('event_categories.id'), nullable=False)
    
    event_category = relationship('EventCategory', back_populates='events', lazy='selectin')
    event_days = relationship('EventDay', back_populates='event', cascade='all,delete', order_by=asc(EventDay.start_time),)
    creator = relationship('User', back_populates='events', lazy='selectin')
    
    @property
    def creator_name(self) -> str:
        return f'{self.creator.first_name} {self.creator.last_name}'
    
    @property
    def category(self) -> str:
        return self.event_category.name