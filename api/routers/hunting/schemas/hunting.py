from pydantic import BaseModel
from datetime import date
from uuid import UUID

class HuntYearCreate(BaseModel):
    name: str
    start_date: date
    end_date: date

class UserTeamYearCreate(BaseModel):
    user_id: UUID
    hunt_year_id: UUID
    hunt_team_id: UUID