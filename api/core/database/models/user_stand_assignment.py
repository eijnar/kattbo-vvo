import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database.base import Base


class UserStandAssignment(Base):
    __tablename__ = 'user_stand_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    assigned_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    stand_number_id = Column(
        UUID(as_uuid=True), ForeignKey('stand_numbers.id'))

    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))

    assigned_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))

    user = relationship('User', back_populates='user_stand_assignments')
    
    stand_number = relationship(
        'StandNumber', back_populates='user_stand_assignments')
    
    hunting_year = relationship(
        'HuntingYear', back_populates='user_stand_assignments')

    __table_args__ = (
        UniqueConstraint('user_id', 'stand_number_id', 'hunting_year_id',
                         name='_user_stand_hyear_area_uc'),
    )
