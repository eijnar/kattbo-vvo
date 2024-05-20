from sqlalchemy import Column, Integer, String, Text

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, CRUDMixin

class Template(Base, TrackingMixin, CRUDMixin):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String, nullable=False)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    content = Column(Text, nullable=False)