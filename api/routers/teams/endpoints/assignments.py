from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from routers.teams.services.team_services import TeamService
from routers.teams.schemas.assignment_schemas import UserTeamAssignmentCreate, UserTeamAssignmentRead
from core.exceptions import NotFoundException
from core.dependencies import get_team_service

router = APIRouter(tags=["Assignments"])


@router.post("/{team_id}/users", response_model=UserTeamAssignmentRead, status_code=status.HTTP_201_CREATED)
async def assign_user_to_hunting_year(
    team_id: UUID,
    assignment: UserTeamAssignmentCreate,
    team_service: TeamService = Depends(get_team_service)
):
    try:
        new_assignment = await team_service.assign_user_to_hunting_year(
            user_id=assignment.user_id,
            team_id=team_id,
            hunting_year_id=assignment.hunting_year_id
        )
        return new_assignment
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
