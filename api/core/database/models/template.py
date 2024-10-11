from sqlalchemy import Column, String, Text, UUID
from uuid import uuid4

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, CRUDMixin

class Template(Base, TrackingMixin, CRUDMixin):
    __tablename__ = 'templates'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    service = Column(String, nullable=False)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=False)