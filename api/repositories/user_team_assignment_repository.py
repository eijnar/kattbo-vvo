from repositories.base_repository import BaseRepository
from core.database.models import UserTeamAssignment
from sqlalchemy.future import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class UserTeamAssignmentRepository(BaseRepository[UserTeamAssignment]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(UserTeamAssignment, db_session)

    async def assign_user_to_team_year(self, user_id: UUID, team_id: UUID, hunting_year_id: UUID) -> UserTeamAssignment:
        # Check if assignment already exists
        existing_assignment = await self.filter(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        if existing_assignment:
            raise ValueError("User is already assigned to this team and hunting year.")

        assignment = await self.create(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        return assignment

    async def get_assignments_by_user(self, user_id: UUID) -> List[UserTeamAssignment]:
        query = select(UserTeamAssignment).where(UserTeamAssignment.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_assignments_by_team_year(self, team_id: UUID, hunting_year_id: UUID) -> List[UserTeamAssignment]:
        query = select(UserTeamAssignment).where(
            UserTeamAssignment.team_id == team_id,
            UserTeamAssignment.hunting_year_id == hunting_year_id
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()
