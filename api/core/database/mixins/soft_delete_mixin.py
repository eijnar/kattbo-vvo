from sqlalchemy.orm import declarative_mixin
from sqlalchemy import Column, Boolean

@declarative_mixin
class SoftDeleteMixin(object):
    is_active = Column(Boolean, default=True, nullable=False)