from sqlalchemy import Column, Integer, String, Boolean

from core.database.base import Base
from core.database.models.mixins import TrackingMixin

class ClientModel(Base, TrackingMixin):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    client_secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    disabled = Column(Boolean, default=True)
    description = Column(String)