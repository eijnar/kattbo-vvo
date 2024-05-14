from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class TrackingMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
