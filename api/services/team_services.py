import uuid
from typing import List
from logging import getLogger

from repositories.team_repository import TeamRepository
from repositories.user_repository import UserRepository
from repositories.user_team_assignment_repository import UserTeamAssignmentRepository
from core.exceptions import NotFoundException, ConflictException
from core.database.models import Team, User, Area, Waypoint, StandNumber, UserTeamAssignment

logger = getLogger(__name__)

class TeamService:
    def __init__(self, team_repository: TeamRepository, user_team_assignment_repository: UserTeamAssignmentRepository):
        self.team_repository = team_repository
        self.user_team_assignment_repository = user_team_assignment_repository

    async def create_team(self, name: str) -> Team:
        existing_teams = await self.team_repository.filter(name=name)
        if existing_teams:
            logger.error("Database conflict: Team already exists")
            raise ConflictException(f"Team with name '{name}' already exists.")
        team = await self.team_repository.create(name=name)
        return team

    async def get_team(self, team_id: uuid.UUID) -> Team:
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundException(detail=f"Team with ID {team_id} not found.")
        return team

    async def get_all_teams(self, limit: int = 100, offset: int = 0) -> List[Team]:
        teams = await self.team_repository.list(limit=limit, offset=offset)
        return teams

    async def update_team(self, team_id: uuid.UUID, name: str) -> Team:
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundException(detail=f"Team with ID {team_id} not found.")
        team = await self.team_repository.update(team, name=name)
        return team

    async def delete_team(self, team_id: uuid.UUID):
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundException(detail=f"Team with ID {team_id} not found.")
        await self.team_repository.delete(team)
        
    async def get_users_for_hunting_year(self, team_id: uuid.UUID, hunting_year_id: uuid.UUID) -> List[User]:
        users = await self.team_repository.get_users_for_hunting_year(team_id, hunting_year_id)
        return users

    async def get_areas(self, team_id: uuid.UUID) -> List[Area]:
        areas = await self.team_repository.get_areas(team_id)
        return areas

    async def get_waypoints(self, team_id: uuid.UUID) -> List[Waypoint]:
        waypoints = await self.team_repository.get_waypoints(team_id)
        return waypoints

    async def get_stand_numbers(self, team_id: uuid.UUID) -> List[StandNumber]:
        stand_numbers = await self.team_repository.get_stand_numbers(team_id)
        return stand_numbers
    
    async def assign_user_to_hunting_year(self, user_id: uuid.UUID, team_id: uuid.UUID, hunting_year_id: uuid.UUID) -> UserTeamAssignment:
        team = await self.team_repository.read(team_id)
        if not team:
            raise NotFoundException(detail=f"Team with ID {team_id} not found.")

        user_repository = UserRepository(self.team_repository.db_session)
        user = await user_repository.read(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found.")

        assignment = await self.user_team_assignment_repository.assign_user_to_team_year(user_id, team_id, hunting_year_id)
        return assignment

    