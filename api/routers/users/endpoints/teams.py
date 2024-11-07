from logging import getLogger
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from uuid import UUID

from services.user_team_assignment_service import UserTeamAssignmentService
from schemas.assignment import UserTeamAssignmentCreate, UserTeamAssignmentRead
from core.dependencies import get_user_team_assignment_service


router = APIRouter(tags=["Assignments"])
logger = getLogger(__name__)

@router.put("/{user_id}/teams", response_model=UserTeamAssignmentRead, status_code=status.HTTP_201_CREATED)
async def assign_user_to_team_and_hunting_year(
    user_id: UUID,
    assignment_data: UserTeamAssignmentCreate,
    user_team_assignment_service: UserTeamAssignmentService = Depends(get_user_team_assignment_service),
):
    """
    # Assigns a user to a team and a hunting year.
    If no `hunting_year_id` is provided, assigns to the current hunting year.
    """

    new_assignment = await user_team_assignment_service.assign_user_to_team_year(
        user_id=user_id,
        team_id=assignment_data.team_id,
        hunting_year_id=assignment_data.hunting_year_id
    )
    return new_assignment
