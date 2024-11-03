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

        
@router.get("/{team_id}/users", response_model=TeamUsersResponse, tags=["Get Assignments"])
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