from uuid import UUID
from typing import List
from logging import getLogger


from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from core.exceptions import DatabaseException
from repositories.base_repository import BaseRepository
from core.database.models import (
    Team,
    User,
    Area,
    Waypoint,
    StandNumber,
    User,
    UserTeamAssignment
)


logger = getLogger(__name__)


class TeamRepository(BaseRepository[Team]):
    def __init__(self, db_session):
        super().__init__(Team, db_session)

    async def get_users_for_hunting_team_and_year(self, team_id: UUID, hunting_year_id: UUID) -> List[User]:
        query = select(User).join(UserTeamAssignment).where(
            UserTeamAssignment.team_id == team_id,
            UserTeamAssignment.hunting_year_id == hunting_year_id
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_areas(self, team_id: UUID) -> List[Area]:

        query = select(Area).where(Area.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_waypoints(self, team_id: UUID) -> List[Waypoint]:

        query = select(Waypoint).where(Waypoint.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_stand_numbers(self, team_id: UUID) -> List[StandNumber]:

        query = select(StandNumber).where(StandNumber.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_all_by_ids(self, ids: List[UUID]) -> List[Team]:
        try:
            query = select(self.model).where(self.model.id.in_(ids))
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve teams: {e}")
            raise DatabaseException(detail="Failed to retrieve teams.") from e
