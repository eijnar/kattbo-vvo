from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID

from services.team_services import TeamService
from services.hunting_year_service import HuntingYearService
from routers.team.schemas.assignment_schemas import UserTeamAssignmentCreate, UserTeamAssignmentRead
from core.exceptions import NotFoundException, ConflictException
from core.dependencies import get_user_team_assignment_service
from services.user_team_assignemnt_service import UserTeamAssignmentService
from core.database.models import HuntingYear
from core.hunting_year_dependency import get_resolved_hunting_year

router = APIRouter(tags=["Assignments"])
logger = getLogger(__name__)

@router.post("/{team_id}/users", response_model=UserTeamAssignmentRead, status_code=status.HTTP_201_CREATED)
async def assign_user_to_team_and_hunting_year(
    team_id: UUID,
    assignment_data: UserTeamAssignmentCreate,
    hunting_year: HuntingYear = Depends(get_resolved_hunting_year),
    user_team_assignment_service: UserTeamAssignmentService = Depends(get_user_team_assignment_service),
):
    """
    Assigns a user to a team and a hunting year.
    If no hunting_year_id is provided, assigns to the current hunting year.
    """
    
    logger.info(f"Route: {hunting_year.id}")
    try:
        new_assignment = await user_team_assignment_service.assign_user_to_hunting_year(
            user_id=assignment_data.user_id,
            team_id=team_id,
            hunting_year_id=hunting_year.id
        )
        return new_assignment
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        ) from e
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.detail
        ) from e
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
        ) from ve
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        ) from e