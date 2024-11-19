from uuid import UUID
from typing import Tuple, List, Optional
from logging import getLogger

from repositories import TeamRepository, UserTeamAssignmentRepository
from services.hunting_year_service import HuntingYearService
from core.exceptions import NotFoundError, ConflictError
from core.database.models import Team, User, Area, Waypoint, StandNumber, HuntingYear

logger = getLogger(__name__)


class TeamService:
    def __init__(self, team_repository: TeamRepository, user_team_assignment_repository: UserTeamAssignmentRepository, hunting_year_service: HuntingYearService):
        self.team_repository = team_repository
        self.user_team_assignment_repository = user_team_assignment_repository
        self.hunting_year_service = hunting_year_service

    async def create_team(self, name: str) -> Team:
        existing_teams = await self.team_repository.exists(name=name)
        if existing_teams:
            logger.error("Database conflict: Team already exists")
            raise ConflictError(f"Team with name '{name}' already exists.")
        team = await self.team_repository.create(name=name)
        return team

    async def get_team(self, team_id: UUID) -> Team:
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundError(
                detail=f"Team with ID {team_id} not found.")
        return team

    async def get_all_teams(self, limit: int = 100, offset: int = 0) -> List[Team]:
        teams = await self.team_repository.list(limit=limit, offset=offset)
        if not teams:
            raise NotFoundError(detail="No teams found")
        return teams

    async def update_team(self, team_id: UUID, name: str) -> Team:
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundError(
                detail=f"Team with ID {team_id} not found.")
        team = await self.team_repository.update(team, name=name)
        return team

    async def delete_team(self, team_id: UUID):
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundError(
                detail=f"Team with ID {team_id} not found.")
        await self.team_repository.delete(team)

    async def get_users_for_hunting_team_and_year(
        self, 
        team_id: UUID, 
        hunting_year_id: Optional[UUID]
    ) -> Tuple[List[User], HuntingYear]:
        
        if not hunting_year_id:
            current_year = await self.hunting_year_service.get_current_hunting_year()
            hunting_year = current_year
            hunting_year_id = current_year.id
        else:
            hunting_year = await self.hunting_year_service.get_hunting_year(hunting_year_id)

        users = await self.team_repository.get_users_for_hunting_team_and_year(team_id, hunting_year_id)
        if not users:
            raise NotFoundError(detail="No users associated with team")

        return users, hunting_year

    async def get_areas(self, team_id: UUID) -> List[Area]:
        areas = await self.team_repository.get_areas(team_id)
        if not areas:
            raise NotFoundError(detail="No areas found")
        return areas

    async def get_waypoints(self, team_id: UUID) -> List[Waypoint]:
        waypoints = await self.team_repository.get_waypoints(team_id)
        return waypoints

    async def get_stand_numbers(self, team_id: UUID) -> List[StandNumber]:
        stand_numbers = await self.team_repository.get_stand_numbers(team_id)
        return stand_numbers
