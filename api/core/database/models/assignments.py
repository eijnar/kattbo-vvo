import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, UUID
from sqlalchemy.orm import relationship

from core.database.base import Base


class WaypointStandAssignment(Base):
    __tablename__ = 'waypoint_stand_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waypoint_id = Column(UUID(as_uuid=True), ForeignKey('waypoints.id'))
    area_id = Column(UUID(as_uuid=True), ForeignKey('areas.id'))
    stand_number_id = Column(
        UUID(as_uuid=True), ForeignKey('stand_numbers.id'))
    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))

    waypoint = relationship('Waypoint', back_populates='stand_assignments')
    area = relationship('Area')
    stand_number = relationship(
        'StandNumber', back_populates='waypoint_stand_assignments')
    hunting_year = relationship(
        'HuntingYear', back_populates='waypoint_stand_assignments')

    __table_args__ = (
        UniqueConstraint('waypoint_id', 'area_id',
                         'hunting_year_id', name='_waypoint_area_hyear_uc'),
    )


class UserTeamAssignment(Base):
    __tablename__ = 'user_team_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assigned_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))    
    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))

    user = relationship('User', back_populates='user_team_assignments')
    team = relationship('Team', back_populates='user_team_assignments')
    hunting_year = relationship('HuntingYear', back_populates='user_team_assignments')

    __table_args__ = (
        UniqueConstraint('user_id', 'hunting_year_id', name='_user_hyear_uc'),
    )


class UserStandAssignment(Base):
    __tablename__ = 'user_stand_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assigned_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    stand_number_id = Column(
        UUID(as_uuid=True), ForeignKey('stand_numbers.id'))
    hunting_year_id = Column(
        UUID(as_uuid=True), ForeignKey('hunting_years.id'))
    assigned_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship('User', back_populates='user_stand_assignments')
    stand_number = relationship(
        'StandNumber', back_populates='user_stand_assignments')
    hunting_year = relationship(
        'HuntingYear', back_populates='user_stand_assignments')

    __table_args__ = (
        UniqueConstraint('user_id', 'stand_number_id', 'hunting_year_id',
                         name='_user_stand_hyear_area_uc'),
    )


class TaskAssignment(Base):
    __tablename__ = 'task_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoint_tasks.id'), nullable=False)
    assigned_to = Column(UUID(as_uuid=True),
                         ForeignKey('users.id'), nullable=False)

    assigned_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    task = relationship("WaypointTask", back_populates="assignments")
    assigned_to_user = relationship("User", foreign_keys=[assigned_to])
