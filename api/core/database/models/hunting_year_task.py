import uuid
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, SoftDeleteMixin


class HuntingYearTask(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'hunting_year_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hunting_year_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunting_years.id'), nullable=False)
    task_template_id = Column(UUID(as_uuid=True), ForeignKey(
        'task_templates.id'), nullable=False)
    order = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=False)

    hunting_year = relationship(
        "HuntingYear", back_populates="hunting_year_tasks")
    task_template = relationship("TaskTemplate")
