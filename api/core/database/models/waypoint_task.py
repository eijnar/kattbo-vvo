import uuid

from sqlalchemy import Column, ForeignKey, UUID, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from core.database.base import Base


class WaypointTask(Base):
    __tablename__ = 'waypoint_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waypoint_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoints.id'), nullable=False)
    description = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    fixed_by = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    fixed_at = Column(DateTime(timezone=True), nullable=True)

    waypoint = relationship("Waypoint", back_populates="tasks")
    created_by_user = relationship("User", foreign_keys=[created_by])
    fixed_by_user = relationship("User", foreign_keys=[fixed_by])
    assignments = relationship("TaskAssignment", back_populates="task")
