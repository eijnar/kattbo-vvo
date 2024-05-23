from typing import Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.config import settings
from core.database.utils.database_operations import sqlalchemy_error_handler
from core.database.models import UserModel, GroupModel



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

    @sqlalchemy_error_handler
    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """
        Fetches a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[UserModel]: The user model if found, None otherwise.
        """
        async with self.db_session as session:
            user = await session.get(UserModel, user_id)
            return user

    @sqlalchemy_error_handler
    async def get_user_by_email(self, email: EmailStr) -> Optional[UserModel]:
        """
        Fetches a user by email.

        Args:
            email (EmailStr): The email of the user.

        Returns:
            Optional[UserModel]: The user model if found, None otherwise.
        """
        async with self.db_session as session:
            result = await session.execute(
                select(UserModel).filter(UserModel.email == email)
            )
            return result.scalars().first()

    async def auth0_register_user(self, user_data):
        """
        Creates a new user in the database with the provided user data.

        Args:
            user_data (dict): A dictionary containing the user's data.

        Returns:
            UserModel: The newly created user object.

        Raises:
            SQLAlchemyError: If there is an error executing the query.
        """
        async with self.db_session as session:
            user = UserModel(**user_data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
