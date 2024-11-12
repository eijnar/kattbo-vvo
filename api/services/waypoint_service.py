from uuid import UUID
from typing import List
from logging import getLogger

from geoalchemy2 import WKTElement
from sqlalchemy.exc import SQLAlchemyError

from repositories.waypoint_repository import WaypointRepository
from core.database.models import Waypoint
from schemas.geodata.waypoint import WaypointCreate, WaypointUpdate  # Assuming these schemas exist
from core.exceptions import NotFoundException

logger = getLogger(__name__)


class WaypointService:
    def __init__(self, waypoint_repository: WaypointRepository):
        self.waypoint_repository = waypoint_repository

    async def get_waypoint(self, waypoint_id: UUID) -> Waypoint:
        waypoint = await self.waypoint_repository.read(waypoint_id)
        if not waypoint:
            raise NotFoundException(detail="Waypoint not found.")
        return waypoint

    async def get_all_waypoints(self) -> List[Waypoint]:
        return await self.waypoint_repository.list()

    async def create_waypoint(self, waypoint_create: WaypointCreate) -> Waypoint:
        location = WKTElement(f'POINT({waypoint_create.longitude} {waypoint_create.latitude})', srid=4326)
        waypoint = await self.waypoint_repository.create(
            name=waypoint_create.name,
            location=location,
            category_id=waypoint_create.category_id,
            team_id=waypoint_create.team_id
        )
        return waypoint

    async def update_waypoint(self, waypoint_id: UUID, waypoint_update: WaypointUpdate) -> Waypoint:
        waypoint = await self.get_waypoint(waypoint_id)
        if waypoint_update.name:
            waypoint.name = waypoint_update.name
        if waypoint_update.latitude and waypoint_update.longitude:
            waypoint.location = WKTElement(
                f'POINT({waypoint_update.longitude} {waypoint_update.latitude})', srid=4326
            )
        if waypoint_update.category_id:
            waypoint.category_id = waypoint_update.category_id
        return await self.waypoint_repository.update(waypoint)

    async def delete_waypoint(self, waypoint_id: UUID):
        waypoint = await self.get_waypoint(waypoint_id)
        await self.waypoint_repository.delete(waypoint)
