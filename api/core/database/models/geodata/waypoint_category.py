from uuid import uuid4

from sqlalchemy import String, Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class WaypointCategory(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'waypoint_categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)

    

    # Self-referential Foreign Key
    parent_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoint_categories.id'), nullable=True)

    # Relationship to Parent
    parent = relationship(
        'WaypointCategory',
        remote_side=[id],
        back_populates='subcategories',
        lazy='selectin'
    )

    # Relationship to Subcategories
    subcategories = relationship(
        'WaypointCategory',
        back_populates='parent',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    # Relationship to Waypoints
    waypoints = relationship(
        'Waypoint',
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
