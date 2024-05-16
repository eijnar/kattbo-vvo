from typing import Optional
from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..utils.database_operations import sqlalchemy_error_handler
from ..models import UserModel, ScopeModel, RoleModel
from ...security.passwords import get_password_hash, verify_password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @sqlalchemy_error_handler
    async def get_all_users(self, page: int = 1, page_size: int = 20):
        async with self.db_session as session:
            result = await session.execute(
                select(UserModel).offset((page - 1) * page_size).limit(page_size)
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

    async def update_user_password(
        self,
        user_id: int,
        new_password: str
    ) -> bool:
        """
        Updates the password of a user.

        Args:
            user_id (int): The ID of the user.
            new_password (str): The new password.

        Returns:
            bool: True if the password was successfully updated, False otherwise.
        """
        
        async with self.db_session as session:
            user = await session.get(UserModel, user_id)
            if user:
                user.hashed_password = get_password_hash(new_password)
                self.db_session.add(user)
                await self.db_session.commit()
                return True
            return False


    @sqlalchemy_error_handler
    async def verify_user_password(
        self, user_id: int, password: str
    ) -> bool:
        """
        Verify if the provided password matches the hashed password of the user with the given user_id.

        Args:
            user_id (int): The ID of the user.
            password (str): The plain text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        user: Optional[UserModel] = await self.db_session.get(UserModel, user_id)
        if user and verify_password(password, user.hashed_password):
            return True
        return False

    @sqlalchemy_error_handler
    async def get_user_scopes(self, user_id):
        async with self.db_session as session:
            query = select(ScopeModel.scope).join(ScopeModel.roles).join(RoleModel.users).where(UserModel.id == user_id)
            result = await session.execute(query)
            scopes = result.scalars().all()
            return scopes
            