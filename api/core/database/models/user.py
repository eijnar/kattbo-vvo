from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, CRUDMixin
from core.database.models.relationships.group_users import group_users


class UserModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    auth0_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    profile_picture = Column(String(255), default='profile_pics/default.png')
    disabled = Column(Boolean, default=True)
    last_login_at = Column(DateTime, default=func.now())
    current_login_at = Column(DateTime, default=func.now())
    last_login_ip = Column(String(16))
    current_login_ip = Column(String(16))
    login_count = Column(Integer)

    # Relationships
    groups = relationship('GroupModel', secondary=group_users,
                         back_populates='users')


class GroupModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    description = Column(String(255))

    users = relationship(
        'UserModel', 
        secondary=group_users,
        back_populates='groups'
    )