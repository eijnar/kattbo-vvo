from uuid import UUID
from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import UserTeamAssignment
from core.exceptions import NotFoundException


class UserTeamAssignmentRepository(BaseRepository[UserTeamAssignment]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(UserTeamAssignment, db_session)

    async def assign_user_to_team_year(self, user_id: UUID, team_id: UUID, hunting_year_id: UUID) -> UserTeamAssignment:
        existing_assignment = await self.filter(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        if existing_assignment:
            raise ValueError(
                "User is already assigned to this team and hunting year.")

        assignment = await self.create(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        return assignment

    async def move_user_to_new_team(self, user_id: UUID, current_team_id: UUID, new_team_id: UUID, hunting_year_id: UUID) -> UserTeamAssignment:
        current_assignment = await self.get_one(
            user_id=user_id,
            team_id=current_team_id,
            hunting_year_id=hunting_year_id
        )

        if not current_assignment:
            raise NotFoundException(current_assignment)

        await self.delete(current_assignment)

        new_assignment = await self.assign_user_to_team_year(user_id, new_team_id, hunting_year_id)

        return new_assignment

    async def get_assignments_by_user(self, user_id: UUID) -> List[UserTeamAssignment]:
        query = select(UserTeamAssignment).where(
            UserTeamAssignment.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_assignments_by_team_year(self, team_id: UUID, hunting_year_id: UUID) -> List[UserTeamAssignment]:
        query = select(UserTeamAssignment).where(
            UserTeamAssignment.team_id == team_id,
            UserTeamAssignment.hunting_year_id == hunting_year_id
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()
