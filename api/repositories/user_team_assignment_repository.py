from logging import getLogger
from uuid import UUID
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import UserTeamAssignment
from core.exceptions import DatabaseException


logger = getLogger(__name__)


class UserTeamAssignmentRepository(BaseRepository[UserTeamAssignment]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(UserTeamAssignment, db_session)

    async def get_assignment(self, user_id: UUID, team_id: UUID, hunting_year_id: UUID) -> Optional[UserTeamAssignment]:
        logger.debug(f"Start querying for existing assignment using: user_id: {user_id}, team_id: {team_id}, hunting_year_id: {hunting_year_id}")
        query = select(UserTeamAssignment).where(
            UserTeamAssignment.user_id == user_id,
            UserTeamAssignment.hunting_year_id == hunting_year_id,
        )
        result = await self.db_session.execute(query)
        instance = result.scalar_one_or_none()
        logger.debug(f"Finished quering for existing assignment")
        return instance

    async def create_assignment(self, user_id: UUID, team_id: UUID, hunting_year_id: UUID) -> UserTeamAssignment:
        logger.debug(
            "Creating UserTeamAssignment",
            extra={
                "user.target.id": str(user_id),
                "resource": [
                    {"type": "team", "id": str(team_id)},
                    {"type": "hunting_year", "id": str(hunting_year_id)}
                ]
            }
        )
        new_assignment = UserTeamAssignment(
            user_id=user_id,
            team_id=team_id,
            hunting_year_id=hunting_year_id
        )
        self.db_session.add(new_assignment)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_assignment)
            logger.debug(
                "Created UserTeamAssignment",
                extra={
                    "user.target.id": str(user_id),
                    "resource": [
                        {"type": "team", "id": str(team_id)},
                        {"type": "hunting_year", "id": str(hunting_year_id)}
                    ]
                }
            )
        except SQLAlchemyError as e:
            logger.error(f"Failed to create assignment: {e}")
            raise DatabaseException(f"Failed to create assignment: {e}")
        
        return new_assignment

    async def update_assignment(self, assignment: UserTeamAssignment, team_id: UUID) -> UserTeamAssignment:
        assignment.team_id = team_id
        try:
            await self.db_session.commit()
            await self.db_session.refresh(assignment)
        except SQLAlchemyError as e:
            logger.error(f"Failed to update assignment: {e}")
            raise DatabaseException(f"Failed to update assignment: {e}")
        return assignment
        
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
