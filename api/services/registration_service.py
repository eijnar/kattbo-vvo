import json
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.security.token_manager import TokenManager
from core.config import settings
from core.security.passwords import get_password_hash
from core.tasks.notification_task import send_notification_task
from repositories.user_repository import UserRepository

class RegistrationService:
    def __init__(self, db_session: AsyncSession, token_manager: TokenManager, redis_client):
        self.user_repository = UserRepository(db_session)
        self.token_manager = token_manager
        self.redis_client = redis_client

    async def register_user(self, user_data):
        user_key = f"unconfirmed_user:{user_data.email}"

        # Check if the user is already in the process of confirming
        existing_user = await self.redis_client.get(user_key)
        if existing_user:
            raise HTTPException(status_code=400, detail="A confirmation email has already been sent. Please check your email.")

        # Hash the user's password
        hashed_password = get_password_hash(user_data.password)
        user_data_dict = user_data.dict()
        user_data_dict.update({"hashed_password": hashed_password})
        
        user_data_dict.pop("password", None)

        # Store user data in Redis with a 1-hour expiration
        await self.redis_client.setex(user_key, timedelta(hours=1), json.dumps(user_data_dict))

        # Create a confirmation token
        confirmation_token = await self.token_manager.create_token(
            user_data.email,
            "confirmation",
            expires_delta=timedelta(hours=1),
            version_ttl=timedelta(hours=1)
        )

        # Generate confirmation link
        confirmation_link = f"{settings.HTTP_PROTOCOL}://{settings.SITE_URL}/v1/confirm-email?token={confirmation_token}"

        # Prepare context for email template
        context = {
            "first_name": user_data.first_name,
            "confirmation_link": confirmation_link
        }

        # Send registration email
        await send_notification_task(
            service_name='email',
            recipients=[user_data.email],
            template_name='registration',
            context=context
        )

        return {"message": "Registration successful. Please check your email to confirm your registration."}
