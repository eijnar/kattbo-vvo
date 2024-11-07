from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from core.database.base import Base

# Define the association table
waypoint_areas = Table(
    'waypoint_areas',
    Base.metadata,
    Column('waypoint_id', UUID(as_uuid=True), ForeignKey('waypoints.id'), primary_key=True),
    Column('area_id', UUID(as_uuid=True), ForeignKey('areas.id'), primary_key=True),
    UniqueConstraint('waypoint_id', 'area_id', name='_waypoint_area_uc'),
)