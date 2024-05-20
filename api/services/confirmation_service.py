import json

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from core.security.token_manager import TokenManager
from repositories.user_repository import UserRepository


class ConfirmationService:
    def __init__(self, db_session: AsyncSession, token_manager: TokenManager, redis_client):
        self.user_repository = UserRepository(db_session)
        self.token_manager = token_manager
        self.redis_client = redis_client

    async def confirm_email(self, token: str):
        # Decode and validate the token
        payload = await self.token_manager.validate_token(token, temp=True)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")

        # Validate the token version
        token_version = payload.get("ver")
        if not await self.token_manager.validate_token_version(user_id, token_version):
            raise HTTPException(status_code=400, detail="Invalid token version")

        # Get user data from Redis
        user_data_json = await self.redis_client.get(f"unconfirmed_user:{user_id}")
        if not user_data_json:
            raise HTTPException(status_code=404, detail="User not found or already confirmed")

        user_data = json.loads(user_data_json)

        # Move user to SQL database
        new_user = await self.user_repository.create_user(user_data)

        # Remove user from Redis
        await self.redis_client.delete(f"unconfirmed_user:{user_id}")
        await self.redis_client.delete(f"user_version:{user_id}")

        return {"message": "Email confirmed successfully"}