from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func

class TrackingMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime, default=func.now())
    current_login_at = Column(DateTime, default=func.now())
    last_login_ip = Column(String(16))
    current_login_ip = Column(String(16))
    login_count = Column(Integer)
