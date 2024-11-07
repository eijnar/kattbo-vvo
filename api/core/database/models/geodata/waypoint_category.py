from uuid import uuid4

from sqlalchemy import String, Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class WaypointCategory(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'waypoint_categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    context = Column(String, nullable=False)
    icon = Column(String, nullable=True)

    parent_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoint_categories.id'), nullable=True)
    parent = relationship('WaypointCategory', remote_side=[
                          id], backref='subcategories')

    waypoints = relationship('Waypoint', back_populates='category')
