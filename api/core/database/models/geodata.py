import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint, UUID, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from core.database.base import Base
from core.database.models.mixins import CRUDMixin


class WaypointAreaModel(Base):
    __tablename__ = 'waypoints_areas'

    waypoint_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoints.id'), primary_key=True)
    area_id = Column(UUID(as_uuid=True), ForeignKey(
        'areas.id'), primary_key=True)


class AreaModel(Base, CRUDMixin):
    __tablename__ = 'areas'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    boundary = Column(Geometry('POLYGON'))

    hunt_team_id = Column(UUID(as_uuid=True), ForeignKey('hunt_teams.id'))

    # One to Many relationship
    hunt_team = relationship('HuntTeam', back_populates='areas')

    # Many to Many relationships
    waypoints = relationship(
        "WaypointModel", secondary="waypoints_areas", back_populates="areas")


class WaypointModel(Base, CRUDMixin):
    __tablename__ = 'stands'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    geopoint = Column(Geometry('POINT'))

    # One to Many relatioships
    tasks = relationship("WaypointTask", back_populates="waypoint")

    # Many to Many relationships
    areas = relationship("AreaModel", secondary="waypoints_areas",
                         back_populates="waypoints")

    __table_args__ = (
        UniqueConstraint('name', 'area_id', name='_stand_number_area_uc'),
    )


class WaypointTaskModel(Base):
    __tablename__ = 'waypoint_tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    waypoint_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoints.id'), nullable=False)
    description = Column(String, nullable=False)
    is_fixed = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    fixed_by = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    fixed_at = Column(TIMESTAMP, nullable=True)

    waypoint = relationship("WaypointModel", back_populates="tasks")
    created_by_user = relationship("UserModel", foreign_keys=[created_by])
    fixed_by_user = relationship("UserModel", foreign_keys=[fixed_by])
    assignments = relationship("TaskAssignment", back_populates="task")


class TaskAssignmentModel(Base):
    __tablename__ = 'task_assignments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey(
        'waypoint_tasks.id'), nullable=False)
    assigned_to = Column(UUID(as_uuid=True),
                         ForeignKey('users.id'), nullable=False)
    # When the task was assigned
    assigned_at = Column(TIMESTAMP, nullable=False)

    task = relationship("WaypointTask", back_populates="assignments")
    assigned_to_user = relationship("UserModel", foreign_keys=[assigned_to])


class TrackModel(Base, CRUDMixin):
    pass
