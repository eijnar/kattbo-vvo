from logging import getLogger
from typing import List

from fastapi import HTTPException

from core.exceptions import DatabaseError, NotFoundError, ConflictError
from core.database.models import User
from repositories.user_repository import UserRepository
from schemas import UserBase, UserCreate, UserUpdate


logger = getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self, page: int, page_size: int) -> List[UserBase]:
        users = await self.user_repository.get_all_users(page=page, page_size=page_size)
        return [UserBase.model_validate(user) for user in users]

    async def get_user_by_id(self, id: str) -> UserBase:
        user = self.user_repository.read(id)
        return user

    async def get_user_by_auth0_id(self, auth0_id: str, raise_if_none: bool = False) -> UserBase:
        """
        Retrieves a user by their Auth0 ID.

        Args:
            auth0_id (str): The user's Auth0 ID.
            raise_if_none (bool, optional): If True, raises a NotFoundError if the user is not found. Defaults to False.

        Returns:
            UserBase: The user object if found, or None if not found and raise_if_none=False.
        """
        
        user = await self.user_repository.get_by_auth0_id(auth0_id)
        if not user and raise_if_none:
            raise NotFoundError(f"User with auth0_id {auth0_id} not found.")
        return user


    async def register_user(self, user_data: UserCreate) -> User:
        """
        Registers a new user.

        Args:
        user_data: UserCreate containing the user data to register.

        Returns:
        User: The newly created user.

        Raises:
        ConflictError: If a user with the same auth0_id already exists.
        """
        
        existing_user = await self.user_repository.get_by_auth0_id(user_data.auth0_id)
        
        if existing_user:
            logger.info("User alread registered", extra={
                        'user.id': str(existing_user.id)})
            raise ConflictError(f"User with auth0_id {user_data.auth0_id} already registered.")

        new_user = User(
            auth0_id=user_data.auth0_id,
            email=user_data.email,
            phone_number=user_data.phone_number,
            is_active=False
        )

        created_user = await self.user_repository.create(new_user)
        return created_user


    async def update_user_profile(
        self,
        user: User,
        user_data: UserUpdate
    ) -> User:
        """
        Updates a user's profile fully (PUT).
        """
        try:
            logger.info(
                f"Starting profile update",
                extra={'user.id': str(user.id)}
            )

            # Retrieve user from the repository
            existing_user = await self.user_repository.get_by_auth0_id(user.auth0_id)
            if not existing_user:
                logger.warning(
                    f"User not found in repository for auth0_id: {user.auth0_id}",
                    extra={'user.auth0_id': user.auth0_id}
                )
                raise HTTPException(status_code=404, detail="User not found")

            logger.debug(f"Successfully retrieved user from repository", extra={
                         'user.id': str(existing_user.id)})

            # Update all fields (full update), assuming all fields in user_data are present
            existing_user.first_name = user_data.first_name
            existing_user.last_name = user_data.last_name
            existing_user.phone_number = user_data.phone_number

            logger.info(f"All fields updated for user", extra={
                        'user.id': str(existing_user.id)})

            # Save the updated user in the repository
            updated_user = await self.user_repository.update_user(existing_user)
            logger.info(f"User profile updated successfully",
                        extra={'user.id': str(updated_user.id)})
            return updated_user

        except DatabaseError as e:
            logger.error(
                f"Database error occurred while updating user {user.id}: {str(e)}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

        except HTTPException as e:
            logger.error(f"HTTP error while updating user: {e.detail}", extra={
                         'user.id': str(user.id)})
            raise e

        except Exception as e:
            logger.exception(
                f"Unexpected error occurred during profile update for user {user.id}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    async def update_user_profile_partial(
        self,
        user: User,
        user_data: UserUpdate
    ) -> User:
        """
        Partially updates a user's profile (PATCH).
        """
        try:
            logger.info(
                f"Starting partial profile update",
                extra={'user.id': str(user.id)}
            )

            # Retrieve user from the repository
            existing_user = await self.user_repository.get_by_auth0_id(user.auth0_id)
            if not existing_user:
                logger.warning(
                    f"User not found in repository for auth0_id: {user.auth0_id}",
                    extra={'user.auth0_id': user.auth0_id}
                )
                raise HTTPException(status_code=404, detail="User not found")

            logger.debug(f"Successfully retrieved user from repository",
                         extra={'user.id': str(existing_user.id)})

            # Perform partial update: only update fields that are provided by the user
            update_data = user_data.model_dump(exclude_unset=True)

            # Create a copy of the existing user and apply the updates
            existing_user = existing_user.model_copy(update=update_data)

            logger.info(f"Fields updated for user", extra={
                        'user.id': str(existing_user.id)})

            # Save the updated user in the repository
            updated_user = await self.user_repository.update_user(existing_user)
            logger.info(f"User profile partially updated successfully",
                        extra={'user.id': str(updated_user.id)})
            return updated_user

        except DatabaseError as e:
            logger.error(
                f"Database error occurred while updating user {user.id}: {str(e)}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

        except HTTPException as e:
            logger.error(f"HTTP error while updating user: {e.detail}", extra={
                'user.id': str(user.id)})
            raise e

        except Exception as e:
            logger.exception(
                f"Unexpected error occurred during profile update for user {user.id}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
