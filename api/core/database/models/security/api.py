from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, String, DateTime, JSON, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship

from core.database.base import Base

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(String, unique=True, index=True, nullable=False)
    hashed_secret = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    permissions = Column(JSON, default=[])
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="api_keys")
