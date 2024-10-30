from uuid import UUID
from typing import Optional
from logging import getLogger

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

        logger.info("Starting to assign the user to Team",            
            extra={
                "user.id": str(user_id),
                "resource": [
                    {"type": "team", "id": str(team_id)},
                ]
            })
                
        if not hunting_year_id:
            logger.debug("No hunting_year_id provided, fetching current_hunting_year", extra={"user_id": user_id})
            current_year = await self.hunting_year_service.get_current_hunting_year()
            hunting_year_id = current_year.id
            logger.debug(f"Fetched current hunting year: {current_year}", extra={"resource": [{"type": "team", "id": str(team_id)}]})

        assignment = await self.user_team_assignment_repository.assign_user_to_team_year(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        
        logger.info(
            "User successfully assigned to Team",
            extra={
                "user.id": str(user_id),
                "resource": [
                    {"type": "team", "id": str(team_id)},
                    {"type": "hunting_year", "id": str(hunting_year_id)}
                ],
                "assignment.id": str(assignment.id)
            }
        )
        return assignment
    
    async def move_user_to_team(
        self
    )
