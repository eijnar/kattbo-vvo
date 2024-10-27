from uuid import UUID

from core.exceptions import NotFoundException, ConflictException, DatabaseException
from repositories import UserTeamAssignmentRepository
from core.database.models.assignments import UserTeamAssignment
from services.user_service import UserService
from services.team_services import TeamService

class UserTeamAssignmentService:
    def __init__(
        self,
        user_team_assignment_repository: UserTeamAssignmentRepository,
        team_service: TeamService,
        user_service: UserService
    ):
        self.user_team_assignemnt_repository = user_team_assignment_repository
        self.team_service = team_service
        self.user_service = user_service
        
    async def assign_user_to_hunting_year(
        self,
        user_id: UUID,
        team_id: UUID,
        hunting_year_id: UUID
    ) -> UserTeamAssignment:
        
        await self.team_service.get_team(team_id)
        await self.user_service.get_user_by_id(user_id)
        return await self.user_team_assignemnt_repository.assign_user_to_team_year(user_id, team_id, hunting_year_id)
    
    async def move_user_to_new_team(
        self,
        user_id: UUID,
        current_team_id: UUID,
        new_team_id: UUID,
        hunting_year_id: UUID
    ) -> UserTeamAssignment:
        
        await self.team_service.get_team(new_team_id)
        return await self.user_team_assignemnt_repository.move_user_to_team_year(
            user_id, current_team_id, new_team_id, hunting_year_id
        )