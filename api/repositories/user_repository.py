from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select

from core.database.utils.database_operations import sqlalchemy_error_handler
from core.database.models import UserModel
from core.exceptions import DatabaseOperationException

logger = getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @sqlalchemy_error_handler
    async def get_all_users(self, page: int = 1, page_size: int = 20):
        """
        Retrieves all users from the database.

        Args:
            page (int, optional): The page number of the results. Defaults to 1.
            page_size (int, optional): The number of users per page. Defaults to 20.

        Returns:
            List[UserModel]: A list of UserModel objects representing the users.

        Raises:
            SQLAlchemyError: If there is an error executing the query.
        """
        async with self.db_session as session:
            result = await session.execute(
                select(UserModel).offset(
                    (page - 1) * page_size).limit(page_size)
            )
            users = result.scalars().all()
            return users

    async def get_by_auth0_id(self, auth0_id: str):
        """
        Retrieves a user from the database based on their Auth0 ID.
        """
        try:
            result = await self.db_session.execute(
                select(UserModel).filter(UserModel.auth0_id == auth0_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while fetching user by Auth0 ID {auth0_id}: {str(e)}")
            raise DatabaseOperationException(
                "Error fetching user by Auth0 ID") from e

    async def create_user(self, new_user: UserModel):
        """
        Creates a new user in the database.
        """
        try:
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            logger.error(
                f"Integrity error while creating user {new_user.email}: {str(e)}")
            raise DatabaseOperationException(
                "Error creating user due to constraint violation") from e
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while creating user {new_user.email}: {str(e)}")
            raise DatabaseOperationException("Error creating user") from e

    async def update_user(self, user: UserModel) -> UserModel:
        """
        Updates a user's information in the database.
        """
        try:
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            raise DatabaseOperationException(f"Error updating user: {str(e)}")
