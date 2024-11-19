from logging import getLogger
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from repositories.base_repository import BaseRepository
from core.database.models import User
from core.exceptions import NotFoundError, DatabaseError


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
