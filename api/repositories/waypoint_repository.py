from uuid import UUID
from typing import List
from logging import getLogger

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from core.exceptions import DatabaseException
from repositories.base_repository import BaseRepository
from core.database.models import Waypoint

logger = getLogger(__name__)


class WaypointRepository(BaseRepository[Waypoint]):
    def __init__(self, db_session):
        super().__init__(Waypoint, db_session)
        
    async def get_all_by_ids(self, ids: List[UUID]) -> List[Waypoint]:
        try:
            query = select(self.model).where(self.model.id.in_(ids))
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve waypoints: {e}")
            raise DatabaseException(detail="Failed to retrieve waypoints.") from e