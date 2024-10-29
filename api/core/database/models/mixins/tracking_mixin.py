from datetime import datetime, timezone

from sqlalchemy.orm import declarative_mixin
from sqlalchemy import Column, DateTime


@declarative_mixin
class TrackingMixin(object):
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
