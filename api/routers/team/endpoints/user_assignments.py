from logging import getLogger
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from uuid import UUID

from services.team_services import TeamService
from services.user_team_assignment_service import UserTeamAssignmentService
from routers.team.schemas.assignment_schemas import TeamUsersResponse
from routers.team.schemas.assignment_schemas import UserTeamAssignmentCreate, UserTeamAssignmentRead
from core.dependencies import get_user_team_assignment_service, get_team_service


router = APIRouter(tags=["Assignments"])
logger = getLogger(__name__)

@router.post("/{team_id}/users", response_model=UserTeamAssignmentRead, status_code=status.HTTP_201_CREATED)
async def assign_user_to_team_and_hunting_year(
    team_id: UUID,
    assignment_data: UserTeamAssignmentCreate,
    user_team_assignment_service: UserTeamAssignmentService = Depends(get_user_team_assignment_service),
):
    """
    # Assigns a user to a team and a hunting year.
    If no `hunting_year_id` is provided, assigns to the current hunting year.
    """

    new_assignment = await user_team_assignment_service.assign_user_to_team(
        user_id=assignment_data.user_id,
        team_id=team_id,
        hunting_year_id=assignment_data.hunting_year_id
    )
    return new_assignment

        
@router.get("/{team_id}/users", response_model=TeamUsersResponse)
async def get_team_users(
    team_id: UUID,
    hunting_year_id: Optional[UUID] = Query(None, description="ID of the hunting year"),
    team_service: TeamService = Depends(get_team_service)
):

    users, hunting_year = await team_service.get_users_for_hunting_team_and_year(team_id, hunting_year_id)
    return TeamUsersResponse(
        hunting_year=hunting_year,
        users=users
    )