from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response


from core.exceptions import NotFoundException
from core.dependencies import get_team_service
from core.hunting_year_dependency import get_resolved_hunting_year
from core.database.models import HuntingYear
from services.team_services import TeamService
from routers.team.schemas.team_schemas import (
    TeamCreate,
    TeamRead,
    TeamUpdate,
    UserRead,
    AreaRead,
    WaypointRead,
    StandNumberRead
)

router = APIRouter()


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamCreate, request: Request, response: Response, team_service: TeamService = Depends(get_team_service)):
    try:
        created_team = await team_service.create_team(name=team.name)
        
        team_url = request.url_for("get_team", team_id=created_team.id)
        
        response.headers["Location"] = str(team_url)
        
        return created_team
    
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.get("/", response_model=List[TeamRead])
async def get_teams(limit: int = 100, offset: int = 0, team_service: TeamService = Depends(get_team_service)):
    teams = await team_service.get_all_teams(limit=limit, offset=offset)
    return teams


@router.get("/{team_id}", response_model=TeamRead)
async def get_team(team_id: str, team_service: TeamService = Depends(get_team_service)):

    try:
        team = await team_service.get_team(team_id)
        return team
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{team_id}", response_model=TeamRead)
async def update_team(team_id: str, team_update: TeamUpdate, team_service: TeamService = Depends(get_team_service)):
    try:
        updated_team = await team_service.update_team(team_id, name=team_update.name)
        return updated_team
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: str, team_service: TeamService = Depends(get_team_service)):

    try:
        await team_service.delete_team(team_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{team_id}/users", response_model=List[UserRead])
async def get_team_users(
    team_id: UUID,
    hunting_year_id: HuntingYear = Depends(get_resolved_hunting_year),
    team_service: TeamService = Depends(get_team_service)
):

    users = await team_service.get_users_for_hunting_year(team_id, hunting_year_id.id)
    return users


@router.get("/{team_id}/areas", response_model=List[AreaRead])
async def get_team_areas(team_id: UUID, team_service: TeamService = Depends(get_team_service)):
    areas = await team_service.get_areas(team_id)
    return areas


@router.get("/{team_id}/waypoints", response_model=List[WaypointRead])
async def get_team_waypoints(team_id: UUID, team_service: TeamService = Depends(get_team_service)):
    waypoints = await team_service.get_waypoints(team_id)
    return waypoints


@router.get("/{team_id}/stand-numbers", response_model=List[StandNumberRead])
async def get_team_stand_numbers(team_id: UUID, team_service: TeamService = Depends(get_team_service)):
    stand_numbers = await team_service.get_stand_numbers(team_id)
    return stand_numbers
