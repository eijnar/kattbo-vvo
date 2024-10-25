from uuid import UUID
from typing import List

from sqlalchemy.future import select

from repositories.base_repository import BaseRepository
from core.database.models import Team, User, Area, Waypoint, StandNumber, User
from core.database.models.assignments import UserTeamAssignment


class TeamRepository(BaseRepository[Team]):
    def __init__(self, db_session):
        super().__init__(Team, db_session)
        
    async def get_users_for_hunting_year(self, team_id: UUID, hunting_year_id: UUID) -> List[User]:
        query = select(User).join(UserTeamAssignment).where(
            UserTeamAssignment.team_id == team_id,
            UserTeamAssignment.hunting_year_id == hunting_year_id
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_areas(self, team_id: UUID) -> List[Area]:
        from core.database.models.area import Area

        query = select(Area).where(Area.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_waypoints(self, team_id: UUID) -> List[Waypoint]:
        from core.database.models.waypoint import Waypoint

        query = select(Waypoint).where(Waypoint.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_stand_numbers(self, team_id: UUID) -> List[StandNumber]:
        from core.database.models.stand_number import StandNumber

        query = select(StandNumber).where(StandNumber.team_id == team_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()