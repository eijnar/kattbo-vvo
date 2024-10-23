import datetime
import uuid

from sqlalchemy import Column, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

class APIKeyModel(Base):
    __tablename__ = 'api_keys'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    identifier = Column(String, unique=True, index=True, nullable=False)
    hashed_key = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    permissions = Column(JSON, default=[])
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="api_keys")
