from uuid import UUID

from sqlalchemy.orm import Session

from core.database.models.user import User
from routers.hunting.schemas.hunting import HuntYearCreate, UserTeamYearCreate


class HuntYearRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_hunt_year(self, hunt_year_data: HuntYearCreate) -> HuntYearCreate:
        new_hunt_year = HuntYear(**hunt_year_data.model_dump())
        self.db.add(new_hunt_year)
        self.db.commit()
        self.db.refresh(new_hunt_year)
        return new_hunt_year

    def add_user_to_hunt_year(self, user_id: UUID, hunt_year_id: UUID, hunt_team_id: UUID) -> UserTeamYearCreate:
        new_user_team_year = UserTeamYear(
            user_id=user_id,
            hunt_year_id=hunt_year_id,
            hunt_team_id=hunt_team_id
        )
        self.db.add(new_user_team_year)
        self.db.commit()
        self.db.refresh(new_user_team_year)
        return new_user_team_year
