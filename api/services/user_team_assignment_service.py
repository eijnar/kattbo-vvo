from uuid import UUID
from typing import Optional
from logging import getLogger

from core.exceptions import NotFoundError, ConflictError
from repositories import UserTeamAssignmentRepository
from services.user_service import UserService
from services.team_services import TeamService
from services.hunting_year_service import HuntingYearService
from schemas import UserTeamAssignmentRead


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

    async def assign_user_to_team_year(
        self,
        user_id: UUID,
        team_id: UUID,
        hunting_year_id: Optional[UUID]
    ) -> UserTeamAssignmentRead:

        logger.info("Starting assign process for User to Team and Year",
                    extra={
                        "user.target.id": str(user_id),
                        "resource": [
                            {"type": "team", "id": str(team_id)},
                        ]
                    })

        if not hunting_year_id:
            logger.debug("No hunting_year_id provided, fetching current_hunting_year", extra={
                         "user.target.id": str(user_id)})
            current_year = await self.hunting_year_service.get_current_hunting_year()
            hunting_year_id = current_year.id
            logger.debug(f"Fetched current hunting year: {current_year}", extra={
                         "resource": [{"type": "team", "id": str(team_id)}]})

        team = await self.team_service.get_team(team_id)
        if not team:
            logger.error(f"Team with id {team_id} not found.")
            raise NotFoundError(
                detail=f"Team with ID {team_id} not found.")

        existing_assignment = await self.user_team_assignment_repository.get_assignment(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )

        if existing_assignment:
            logger.debug("Existing assignment found, attemting to update")
            if existing_assignment.team_id == team_id:
                logger.error(
                    f"User {user_id} is already assigned to team {team_id} for {hunting_year_id}")
                raise ConflictError(
                    detail=f"User is already assigned to team."
                )
            else:
                updated_assignment = await self.user_team_assignment_repository.update_assignment(assignment=existing_assignment, team_id=team_id)
                logger.info("Updated UserTeamAssignment to new team")
                return updated_assignment

        else:
            logger.debug("No current assignment found, attemting to create")
            new_assignment = await self.user_team_assignment_repository.create_assignment(user_id=user_id, team_id=team_id, hunting_year_id=hunting_year_id)
            logger.info(
                "User successfully assigned to Team and Year",
                extra={
                    "user.id": str(user_id),
                    "resource": [
                        {"type": "team", "id": str(team_id)},
                        {"type": "hunting_year", "id": str(hunting_year_id)}
                    ],
                    "assignment.id": str(new_assignment.id)
                }
            )
            return new_assignment
