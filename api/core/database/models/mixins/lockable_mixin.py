from sqlalchemy.orm import declarative_mixin
from sqlalchemy import Column, Boolean

@declarative_mixin
class LockableMixin(object):
    is_locked = Column(Boolean, default=False, nullable=False)