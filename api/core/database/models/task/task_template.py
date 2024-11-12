from uuid import uuid4
import enum

from sqlalchemy import Column, String, UUID, Boolean, Enum
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.enum.task_type import TaskType
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class TaskTemplate(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'task_templates'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_mandatory = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)

    hunting_year_tasks = relationship(
        'HuntingYearTask', back_populates='task_template', cascade='all, delete-orphan')
