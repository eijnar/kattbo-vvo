from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, CRUDMixin
from core.database.models.relationships.role_users import role_users
from core.database.models.relationships.role_scopes import role_scopes


class UserModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(420))
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
    roles = relationship('RoleModel', secondary=role_users,
                         back_populates='users')


class RoleModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    description = Column(String(255))

    users = relationship(
        'UserModel', 
        secondary=role_users,
        back_populates='roles'
    )

    scopes = relationship(
        "ScopeModel", 
        secondary='role_scopes', 
        back_populates="roles"
    )


class ScopeModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'scopes'
    id = Column(Integer, primary_key=True)
    scope = Column(String(20), unique=True)
    description = Column(String(255))

    # Relationships
    roles = relationship(
        "RoleModel", 
        secondary=role_scopes, 
        back_populates="scopes"
    )
