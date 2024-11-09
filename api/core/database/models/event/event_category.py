from uuid import uuid4

from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class EventCategory(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'event_categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String, nullable=False)
    
    events = relationship('Event', back_populates='event_category', lazy=True)
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey(
    'event_categories.id'), nullable=True)

    # Relationship to Parent
    parent = relationship(
        'EventCategory',
        remote_side=[id],
        back_populates='subcategories',
        lazy='selectin'
    )

    # Relationship to Subcategories
    subcategories = relationship(
        'EventCategory',
        back_populates='parent',
        cascade='all, delete-orphan',
        lazy='selectin'
    )