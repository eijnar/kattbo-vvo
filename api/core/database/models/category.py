import uuid

from sqlalchemy import String, Column, UUID, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, SoftDeleteMixin

class Category(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    context = Column(String, nullable=False)

    parent_id = Column(UUID(as_uuid=True), ForeignKey(
        'categories.id'), nullable=True)
    parent = relationship('Category', remote_side=[
                          id], backref='subcategories')

    waypoints = relationship('Waypoint', back_populates='category')
    waypoint_metadata = relationship(
        'WaypointCategoryMetadata', back_populates='category')


class WaypointCategoryMetadata(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'waypoint_category_metadata'

    is_active = Column(Boolean, default=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey(
        'categories.id'), primary_key=True)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

    category = relationship(
        'Category', back_populates='waypoint_metadata')
