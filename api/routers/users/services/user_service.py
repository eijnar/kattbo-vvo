from logging import getLogger
from typing import List

from fastapi import HTTPException

from core.exceptions import DatabaseException
from ..schemas.user import UserBaseSchema, UserCreateSchema, UserUpdateSchema
from repositories.user_repository import UserRepository
from core.database.models import UserModel

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
                f"Starting update_user_profile for user: {user}, user_data: {user_data}")
            # Retrieve the existing user from the repository
            existing_user = await self.user_repository.get_by_auth0_id(user.auth0_id)
            if not existing_user:
                logger.warning(
                    f"User not found in repository with auth0_id: {user.auth0_id}")
                raise HTTPException(status_code=404, detail="User not found")
            else:
                logger.debug(f"Retrieved existing user: {existing_user}")

            # Update allowed fields if they are provided
            update_fields = False
            updated_fields = []
            if user_data.phone_number is not None:
                logger.debug(
                    f"Updating phone_number to: {user_data.phone_number}")
                existing_user.phone_number = user_data.phone_number
                update_fields = True
                updated_fields.append('phone_number')
            if user_data.first_name is not None:
                logger.debug(f"Updating first_name to: {user_data.first_name}")
                existing_user.first_name = user_data.first_name
                update_fields = True
                updated_fields.append('first_name')
            if user_data.last_name is not None:
                logger.debug(f"Updating last_name to: {user_data.last_name}")
                existing_user.last_name = user_data.last_name
                update_fields = True
                updated_fields.append('last_name')

            if not update_fields:
                logger.warning("No valid fields provided for update")
                raise HTTPException(
                    status_code=400,
                    detail="No valid fields provided for update"
                )
            else:
                logger.debug(f"Fields updated: {updated_fields}")

            # Save the updated user in the repository
            logger.debug(f"Saving updated user: {existing_user.id}")
            updated_user = await self.user_repository.update_user(existing_user)
            logger.debug(f"User updated successfully: {updated_user.id}")
            return updated_user

        except DatabaseException as e:
            logger.error(
                f"Failed to update user due to a database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Database error while updating user"
            )
        except HTTPException as e:
            logger.error(f"HTTPException encountered: {e.detail}")
            # Re-raise HTTP exceptions to be handled by FastAPI
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error occurred while updating user: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update user due to an unexpected error"
            )
