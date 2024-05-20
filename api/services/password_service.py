import logging

from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.security.token_manager import TokenManager
from repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)


class PasswordService:
    def __init__(self, db_session: AsyncSession, token_manager: TokenManager, redis_client):
        self.user_repository = UserRepository(db_session)
        self.token_manager = token_manager
        self.redis_client = redis_client

    async def request_password_reset(self, email: str):
        user = await self.user_repository.get_user_by_email(email)
        if user:
            token_type = "password_reset"
            password_reset_token_lifetime = timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_LIFESPAN_MINUTES)
            reset_token = await self.token_manager.create_token(
                user.id, token_type, expires_delta=password_reset_token_lifetime
            )
            logger.info(
                f"Password reset requested for user {user.id}. Email queued. {reset_token}")

            # Schedule sending the email in the background
            # background_tasks.add_task(send_password_reset_email, user.email, reset_token)

        return {"message": "If your email is registered with us, you will receive a password reset link shortly."}

    async def reset_password(self, token: str, new_password: str):
        try:
            payload = await self.token_manager.validate_token(token)
            if "password_reset" not in payload.get("scope", []):
                raise HTTPException(status_code=403, detail="Invalid token")

            user_id = payload['sub']
            await self.user_repository.update_user_password(int(user_id), new_password)
            await self.token_manager.invalidate_all_tokens_for_user(int(user_id))

            return {"message": "Password successfully reset"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def update_user_password(self, user_id: int, new_password: str) -> bool:
        return await self.user_repository.update_user_password(user_id, new_password)