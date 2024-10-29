from uuid import UUID
from typing import Optional
from logging import getLogger

from core.exceptions import NotFoundException, ConflictException, DatabaseException
from repositories import UserTeamAssignmentRepository
from core.database.models.user_team_assignment import UserTeamAssignment
from services.user_service import UserService
from services.team_services import TeamService
from services.hunting_year_service import HuntingYearService


logger = getLogger(__name__)
class UserTeamAssignmentService:
    def __init__(
        self,
        user_team_assignment_repository: UserTeamAssignmentRepository,
        team_service: TeamService,
        user_service: UserService,
        hunting_year_service: HuntingYearService
    ):
        self.user_team_assignment_repository = user_team_assignment_repository
        self.team_service = team_service
        self.user_service = user_service
        self.hunting_year_service = hunting_year_service

    async def assign_user_to_team(
        self, 
        user_id: UUID,
        team_id: UUID, 
        hunting_year_id: Optional[UUID]
    ) -> UserTeamAssignment:

        if not hunting_year_id:
            current_year = await self.hunting_year_service.get_current_hunting_year()
            if not current_year:
                raise NotFoundException(detail="Current hunting year not found")
            hunting_year_id = current_year.id
            
        existing_assignment = await self.user_team_assignment_repository.filter(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        if existing_assignment:
            raise ConflictException(detail="User is already assigned to this team and hunting year.")
        
        assignment = await self.user_team_assignment_repository.create(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        return assignment