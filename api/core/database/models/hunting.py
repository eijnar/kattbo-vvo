import uuid
from datetime import datetime

from sqlalchemy import Column, String, Date, ForeignKey, Integer, UniqueConstraint, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from core.database.base import Base
from core.database.models.mixins import CRUDMixin


class HuntYearModel(Base, CRUDMixin):
    __tablename__ = 'hunt_years'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(10), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    stand_assignments = relationship(
        'StandAssignment', backref='hunt_year', lazy=True)
    animal_quotas = relationship('AnimalQuota', back_populates='hunt_year')


class HuntTeamModel(Base, CRUDMixin):
    __tablename__ = 'hunt_teams'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)

    # Relationships
    areas = relationship('Area', back_populates='hunt_team', lazy=True)
    animal_quotas = relationship('AnimalQuota', back_populates='hunt_team')


class UserTeamYearModel(Base, CRUDMixin):
    __tablename__ = 'user_team_years'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    hunt_team_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunt_teams.id'), nullable=False)
    hunt_year_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunt_years.id'), nullable=False)

    hunt_team = relationship('HuntTeam')
    hunt_year = relationship('HuntYear')

    __table_args__ = (
        UniqueConstraint('user_id', 'hunt_year_id',
                         name='unique_user_per_year'),
    )




class StandAssignmentModel(Base, CRUDMixin):
    __tablename__ = 'stand_assignments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    stand_id = Column(UUID(as_uuid=True), ForeignKey(
        'stands.id'), nullable=False)
    hunt_year_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunt_years.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'stand_id', 'hunt_year_id',
                         name='_user_stand_year_uc'),
    )


class AnimalQuotaModel(Base, CRUDMixin):
    __tablename__ = 'animal_quotas'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hunt_year_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunt_years.id'), nullable=False)
    animal_type_id = Column(UUID(as_uuid=True), ForeignKey(
        'animal_types.id'), nullable=False)
    initial_quota = Column(Integer, nullable=True)

    hunt_year = relationship('HuntYear', back_populates='animal_quotas')
    animal_type = relationship('AnimalType', back_populates='quotas')
    hunt_team_id = Column(UUID(as_uuid=True), ForeignKey(
        'hunt_teams.id'), nullable=False)
    hunt_team = relationship('HuntTeam', back_populates='animal_quotas')
    animals_shot = relationship('AnimalShot', back_populates='quota')


class AnimalTypeModel(Base, CRUDMixin):
    __tablename__ = 'animal_types'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    group = Column(String(100), nullable=False)

    quotas = relationship('AnimalQuota', back_populates='animal_type')


class AnimalShotModel(Base, CRUDMixin):
    __tablename__ = 'animals_shot'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_shot = Column(DateTime, default=datetime.utcnow, nullable=False)
    weight = Column(Float)
    age = Column(Integer)
    gender = Column(String(20), nullable=False)
    animal_type_id = Column(UUID(as_uuid=True), ForeignKey('animal_types.id'))
    antler_type = Column(String(255))
    antlers = Column(Integer)
    milk = Column(Boolean, default=False)

    animal_type = relationship('AnimalType')
    quota_id = Column(UUID(as_uuid=True), ForeignKey(
        'animal_quotas.id'), nullable=False)
    quota = relationship('AnimalQuota', back_populates='animals_shot')
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
