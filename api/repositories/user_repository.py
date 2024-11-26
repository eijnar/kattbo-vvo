from logging import getLogger
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from repositories.base_repository import BaseRepository
from core.database.models import User, UserHuntingYearAssignment, UserTeamAssignment
from core.exceptions import NotFoundError, DatabaseError
from schemas import UserProfile


logger = getLogger(__name__)


class UserRepository(BaseRepository[User]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def get_by_id(self, id: str) -> Optional[User]:
        """
        Retrieves a user by their Auth0 ID.
        """
        try:
            result = await self.db_session.execute(
                select(User).filter(User.id == id)
            )
            user = result.scalars().first()
            if not user:
                logger.warning(f"User with ID {id} not found.")
                raise NotFoundError(
                    detail=f"User with ID {id} not found.")
            return user
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to retrieve user with ID {id}: {e}")
            raise DatabaseError(
                detail=f"Failed to retrieve user with ID {id}.") from e

    async def get_by_auth0_id(self, auth0_id: str) -> Optional[User]:
        """sumary_line

        Keyword arguments:
        auth0_id -- The Auth0 ID of the user
        Return: User object or None if not found
        """
        try:
            result = await self.db_session.execute(
                select(User).filter(User.auth0_id == auth0_id)
            )
            user = result.scalars().first()
            return user
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to retrieve user with Auth0 ID {auth0_id}: {e}")
            raise DatabaseError(
                detail=f"Failed to retrieve user with Auth0 ID {auth0_id}.") from e

    async def get_all_users(self, page: int = 1, page_size: int = 20) -> List[User]:
        """
        Retrieves all users from the database with pagination.

        Args:
            page (int, optional): The page number of the results. Defaults to 1.
            page_size (int, optional): The number of users per page. Defaults to 20.

        Returns:
            List[User]: A list of User objects representing the users.
        """
        offset = (page - 1) * page_size
        users = await self.list(limit=page_size, offset=offset)
        logger.info(
            f"Retrieved {len(users)} users (page: {page}, page_size: {page_size}).")
        return users

    async def update_user(self, user: User, **kwargs) -> User:
        """
        Updates a user's information.

        Args:
            user (User): The user instance to update.
            **kwargs: Fields to update with their new values.

        Returns:
            User: The updated user instance.
        """
        updated_user = await self.update(user, **kwargs)

        logger.info(
            f"Updated user",
            extra={
                "user.id": str(updated_user.id)
            })

        return updated_user

    async def delete_user(self, user: User):
        """
        Soft deletes a user by setting 'is_active' to False.

        Args:
            user (User): The user instance to delete.
        """
        await self.delete(user)
        logger.info(f"Soft deleted user with ID {user.id}.")
        
    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        stmt = (
            select(User)
            .options(
                joinedload(User.hunting_year_assignments)
                    .joinedload(UserHuntingYearAssignment.hunting_year),
                joinedload(User.user_team_assignments)
                    .joinedload(UserTeamAssignment.team)
            )
            .where(User.id == user_id)
        )
        
        result = await self.db_session.execute(stmt)
        user = result.scalars().first()
        
        if not user:
            return None
        
        # Identify the current hunting year
        current_assignment = next(
            (assignment for assignment in user.hunting_year_assignments if assignment.hunting_year.is_current),
            None
        )
        
        if current_assignment:
            hunting_year = current_assignment.hunting_year
            # Find the team assigned for the current hunting year
            assigned_team = next(
                (ta.team for ta in user.user_team_assignments if ta.team.hunting_year_id == hunting_year.id),
                None
            )
        else:
            hunting_year = None
            assigned_team = None

        # Construct the UserProfile
        user_profile = UserProfile(
            auth0_id=user.auth0_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            is_active=user.is_active,
            hunting_year=HuntingYearBase(
                id=str(hunting_year.id),
                year=int(hunting_year.year),
                is_current=hunting_year.is_current
            ) if hunting_year else None,
            assigned_team=TeamBase(
                id=str(assigned_team.id),
                name=assigned_team.name,
                hunting_year_id=str(assigned_team.hunting_year_id)
            ) if assigned_team else None
        )

        return user_profile