import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database.base import Base


class WaypointTaskAssignment(Base):
    __tablename__ = 'waypoint_task_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoint_tasks.id'), nullable=False)
    
    assigned_to = Column(UUID(as_uuid=True),
                         ForeignKey('users.id'), nullable=False)

    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task = relationship("WaypointTask", back_populates="assignments")
    assigned_to_user = relationship("User", foreign_keys=[assigned_to])
