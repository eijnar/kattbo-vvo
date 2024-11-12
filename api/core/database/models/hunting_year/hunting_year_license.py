import uuid
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin
from core.database.enum.licence_type import LicenseType

class HuntingYearLicense(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'hunting_year_licenses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hunting_year_id = Column(UUID(as_uuid=True), ForeignKey('hunting_years.id'), nullable=False)
    license_type = Column(Enum(LicenseType), nullable=False)
    cost = Column(Integer, nullable=False)

    hunting_year = relationship('HuntingYear', back_populates='licenses')

    __table_args__ = (
        UniqueConstraint('hunting_year_id', 'license_type', name='_hyear_license_uc'),
    )