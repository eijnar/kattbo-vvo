from uuid import uuid4

from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.base import Base


class UserHuntingYearTask(Base):
    __tablename__ = 'user_hunting_year_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    hunting_year_task_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunting_year_tasks.id'), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    proof = Column(String, nullable=True)

    completed_by = Column(UUID(as_uuid=True),
                          ForeignKey('users.id'), nullable=False)

    user = relationship(
        'User',
        back_populates='assigned_tasks',
        foreign_keys=[user_id]
    )
    completed_by_user = relationship(
        'User',
        back_populates='completed_tasks',
        foreign_keys=[completed_by]
    )
    hunting_year_task = relationship(
        'HuntingYearTask', back_populates='user_hunting_year_tasks')
