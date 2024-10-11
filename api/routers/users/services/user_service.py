from logging import getLogger
from typing import List

from fastapi import HTTPException

from utils.mask_sensitive_data import mask_sensitive_data
from core.exceptions import DatabaseException
from core.database.models import UserModel
from repositories.user_repository import UserRepository
from routers.users.schemas.user import UserBaseSchema, UserCreateSchema, UserUpdateSchema


logger = getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self, page: int, page_size: int) -> List[UserBaseSchema]:
        users = await self.user_repository.get_all_users(page=page, page_size=page_size)
        return [UserBaseSchema.model_validate(user) for user in users]

    async def get_user_by_auth0_id(self, auth0_id: str) -> UserBaseSchema:
        try:
            user = await self.user_repository.get_by_auth0_id(auth0_id)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            logger.error(
                f"Failed to fetch user by auth0_id: {auth0_id}. Error: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to fetch user"
            )

    async def register_user(self, user: UserCreateSchema) -> UserModel:
        """
        Registers a new user by creating them in the repository.
        """
        try:
            existing_user = await self.user_repository.get_by_auth0_id(user.auth0_id)
            if existing_user:
                logger.info("User alread registered", extra={
                            'user.id': str(existing_user.id)})
                raise HTTPException(
                    status_code=400, detail="User already registered")

            # Create new user
            new_user = UserModel(
                auth0_id=user.auth0_id,
                email=user.email,
                phone_number=user.phone_number,
                disabled=False
            )

            return await self.user_repository.create_user(new_user)

        except DatabaseException as e:
            logger.error(
                f"Failed to register user due to a database error: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Database error while registering user")
        except Exception as e:
            logger.error(
                f"Unexpected error occurred while registering user: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Failed to register user due to an unexpected error")

    async def update_user_profile(
        self,
        user: UserModel,
        user_data: UserUpdateSchema
    ) -> UserModel:
        """
        Updates a user's profile in the repository.
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

            logger.debug(f"Successfully retrieved user from repository", extra={'user.id': str(existing_user.id)})

            # Update allowed fields
            updated_fields = []
            if user_data.phone_number:
                logger.debug(f"Updating phone number for user", extra={'user.id': str(existing_user.id)})
                
                # Mask phone number for logging
                masked_phone_number = mask_sensitive_data(user_data.phone_number, 'phone')
                logger.debug(f"Phone number updated to {masked_phone_number} for user", extra={'user.id': str(existing_user.id)})

                # Use the actual phone number for updating the user
                existing_user.phone_number = user_data.phone_number
                updated_fields.append('phone_number')

            # First name update logic
            if user_data.first_name:
                logger.debug(f"Updating first name for user", extra={'user.id': str(existing_user.id)})
                
                # Mask first name for logging
                masked_first_name = mask_sensitive_data(user_data.first_name, 'name')
                logger.debug(f"First name updated to {masked_first_name} for user", extra={'user.id': str(existing_user.id)})

                existing_user.first_name = user_data.first_name  # Actual update
                updated_fields.append('first_name')

            # Last name update logic
            if user_data.last_name:
                logger.debug(f"Updating last name for user", extra={'user.id': str(existing_user.id)})
                
                # Mask last name for logging
                masked_last_name = mask_sensitive_data(user_data.last_name, 'name')
                logger.debug(f"Last name updated to {masked_last_name} for user", extra={'user.id': str(existing_user.id)})

                existing_user.last_name = user_data.last_name  # Actual update
                updated_fields.append('last_name')

            # Handle case where no valid fields were provided
            if not updated_fields:
                logger.warning("No valid fields provided for update", extra={'user.id': str(existing_user.id)})
                raise HTTPException(status_code=400, detail="No valid fields provided for update")


            logger.info(f"Fields updated: {', '.join(updated_fields)}", extra={'user.id': str(existing_user.id)})

            # Save the updated user in the repository
            updated_user = await self.user_repository.update_user(existing_user)
            logger.info(f"User profile updated successfully", extra={'user.id': str(updated_user.id)})
            return updated_user

        except DatabaseException as e:
            logger.error(
                f"Database error occurred while updating user {user.id}: {str(e)}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )  # Keep the error message generic

        except HTTPException as e:
            # HTTP exceptions should be logged and raised as is.
            logger.error(f"HTTP error while updating user: {e.detail}", extra={'user.id': str(user.id)})
            raise e

        except Exception as e:
            logger.exception(
                f"Unexpected error occurred during profile update for user {user.id}",
                extra={'user.id': str(user.id)}
            )
            raise HTTPException(
                status_code=500,
                detail="Internal server error"  # Don't expose the full error to the user
            )

