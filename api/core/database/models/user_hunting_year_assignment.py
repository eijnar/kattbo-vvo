import uuid
from sqlalchemy import Column, ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database.base import Base
from core.database.models.enum.licence_type import LicenseType


class UserHuntingYearAssignment(Base):
    __tablename__ = 'user_hunting_year_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    hunting_year_id = Column(UUID(as_uuid=True), ForeignKey('hunting_years.id'), nullable=False)
    license_type = Column(Enum(LicenseType), nullable=False)
    assigned_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='hunting_year_assignments')
    hunting_year = relationship('HuntingYear', back_populates='user_assignments')

    __table_args__ = (
        UniqueConstraint('user_id', 'hunting_year_id', name='_user_hyear_uc'),
    )