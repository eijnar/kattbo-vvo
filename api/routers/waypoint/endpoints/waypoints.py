from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from core.exceptions import NotFoundException
from core.dependencies import get_waypoint_service
from schemas.geodata.waypoint import WaypointCreate, WaypointUpdate, WaypointResponse
from services.waypoint_service import WaypointService


router = APIRouter()


@router.post("/waypoints/", response_model=WaypointResponse, status_code=status.HTTP_201_CREATED)
async def create_waypoint(
    waypoint_create: WaypointCreate,
    waypoint_service: WaypointService = Depends(get_waypoint_service)
):
    return await waypoint_service.create_waypoint(waypoint_create)


@router.get("/waypoints/{waypoint_id}", response_model=WaypointResponse)
async def get_waypoint(
    waypoint_id: UUID,
    waypoint_service: WaypointService = Depends(get_waypoint_service)
):
    try:
        return await waypoint_service.get_waypoint(waypoint_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/waypoints/{waypoint_id}", response_model=WaypointResponse)
async def update_waypoint(
    waypoint_id: UUID,
    waypoint_update: WaypointUpdate,
    waypoint_service: WaypointService = Depends(get_waypoint_service)
):
    try:
        return await waypoint_service.update_waypoint(waypoint_id, waypoint_update)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/waypoints/{waypoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_waypoint(
    waypoint_id: UUID,
    waypoint_service: WaypointService = Depends(get_waypoint_service)
):
    try:
        await waypoint_service.delete_waypoint(waypoint_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
