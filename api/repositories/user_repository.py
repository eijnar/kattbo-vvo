from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from core.database.models.mixins.crud_mixin import CRUDMixin
from core.database.models import UserModel


from logging import getLogger

logger = getLogger(__name__)


class UserRepository(CRUDMixin[UserModel]):
    model = UserModel

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

    async def get_all_users(self, page: int = 1, page_size: int = 20) -> List[UserModel]:
        """
        Retrieves all users from the database with pagination.

        Args:
            page (int, optional): The page number of the results. Defaults to 1.
            page_size (int, optional): The number of users per page. Defaults to 20.

        Returns:
            List[UserModel]: A list of UserModel objects representing the users.
        """
        offset = (page - 1) * page_size
        users = await self.list(limit=page_size, offset=offset)
        logger.info(f"Retrieved {len(users)} users (page: {page}, page_size: {page_size}).")
        return users

    async def update_user(self, user: UserModel, **kwargs) -> UserModel:
        """
        Updates a user's information.

        Args:
            user (UserModel): The user instance to update.
            **kwargs: Fields to update with their new values.

        Returns:
            UserModel: The updated user instance.
        """
        updated_user = await self.update(user, **kwargs)
        logger.info(f"Updated user with ID {updated_user.id}.")
        return updated_user
    
    async def delete_user(self, user: UserModel):
        """
        Soft deletes a user by setting 'is_active' to False.

        Args:
            user (UserModel): The user instance to delete.
        """
        await self.delete(user)
        logger.info(f"Soft deleted user with ID {user.id}.")