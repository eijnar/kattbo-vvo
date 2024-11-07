from uuid import uuid4

from sqlalchemy import Column, String, Text, UUID

from core.database.base import Base
from core.database.mixins import TrackingMixin, SoftDeleteMixin


class Template(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'templates'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid4, unique=True, nullable=False)
    service = Column(String, nullable=False)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=False)
