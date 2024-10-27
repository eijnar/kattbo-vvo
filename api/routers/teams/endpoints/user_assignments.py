from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from services.team_services import TeamService
from routers.teams.schemas.assignment_schemas import UserTeamAssignmentCreate, UserTeamAssignmentRead
from core.exceptions import NotFoundException, ConflictException
from core.dependencies import get_team_service, get_user_team_assignment_repository
from repositories.user_team_assignment_repository import UserTeamAssignmentRepository

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


@router.post("/{team_id}/users/{user_id}/move", response_model=UserTeamAssignmentRead, status_code=status.HTTP_200_OK)
async def move_user_to_new_team(
    team_id: UUID,
    user_id: UUID,
    new_team_id: UUID,
    hunting_year_id: UUID,
    user_team_assignment_service: UserTeamAssignmentRepository = Depends(get_user_team_assignment_repository)
):
    try:
        new_assignment = await user_team_assignment_service.move_user_to_new_team(
            user_id=user_id,
            current_team_id=team_id,
            new_team_id=new_team_id,
            hunting_year_id=hunting_year_id
        )
    
        return new_assignment
    
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
        
    except ConflictException as ce:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ce.detail)