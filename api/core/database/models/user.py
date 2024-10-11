from uuid import uuid4

from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core.database.base import Base
from core.database.models.mixins import CRUDMixin


class UserModel(Base, CRUDMixin):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    auth0_id = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    profile_picture = Column(String(255), default='profile_pics/default.png')
    disabled = Column(Boolean, default=True)
    
    stands_assigned = relationship('StandAssignment', backref='user', lazy=True)
    animals_shot = relationship('AnimalShot', backref='user', lazy=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)