from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ...database.base import Base
from .dependencies import TrackingMixin, CRUDMixin

roles_users = Table('roles_users', Base.metadata,
                    Column('user_id', Integer, ForeignKey(
                        'user.id'), primary_key=True),
                    Column('role_id', Integer, ForeignKey(
                        'role.id'), primary_key=True)
                    )

roles_scopes = Table('roles_scopes', Base.metadata,
                     Column('role_id', ForeignKey(
                         'role.id'), primary_key=True),
                     Column('scope_id', ForeignKey(
                         'scope.id'), primary_key=True)
                     )


class UserModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'user'
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
    roles = relationship('RoleModel', secondary=roles_users,
                         back_populates='users')


class RoleModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    description = Column(String(255))

    users = relationship('UserModel', secondary=roles_users,
                         back_populates='roles')
    scopes = relationship(
        "ScopeModel", secondary='roles_scopes', back_populates="roles")


class ScopeModel(Base, CRUDMixin, TrackingMixin):
    __tablename__ = 'scope'
    id = Column(Integer, primary_key=True)
    scope = Column(String(20), unique=True)
    description = Column(String(255))

    # Relationships
    roles = relationship(
        "RoleModel", secondary='roles_scopes', back_populates="scopes")
