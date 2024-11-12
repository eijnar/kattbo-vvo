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
        
    