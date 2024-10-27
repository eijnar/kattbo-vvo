import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core.database.base import Base
from core.database.models.mixins import TrackingMixin, SoftDeleteMixin

class User(Base, TrackingMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True, nullable=False)
    auth0_id = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    profile_picture = Column(String(255), default='profile_pics/default.png')

    api_keys = relationship("APIKey", back_populates="user")
    user_team_assignments = relationship('UserTeamAssignment', back_populates='user', cascade="all, delete-orphan")
    user_stand_assignments = relationship('UserStandAssignment', back_populates='user', cascade="all, delete-orphan")
    # animals_shot = relationship('AnimalShot', backref='user', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
