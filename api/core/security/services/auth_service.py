from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from core.security.models.client import ClientModel
from core.redis.client import get_redis_client
import random
import string
from core.security.repositories.client_repository import ClientRepository
import logging

logger = logging.getLogger(__name__)
class AuthorizationService:
    def __init__(self, db_session: AsyncSession, redis_client):
        self.client_repository = ClientRepository(db_session)
        self.redis_client = redis_client

    def generate_random_string(self, length=30):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    async def validate_client(self, client_id: str, redirect_uri: str):
        client = await self.client_repository.get_client(client_id)
        if not client or client.redirect_uri != redirect_uri:
            logger.debug("ERROR!")
            raise HTTPException(status_code=400, detail="Invalid client or redirect URI")
        return client

    async def create_authorization_code(self, user_id: str, client_id: str, scope: str):
        auth_code = self.generate_random_string()
        # Store auth code in Redis with a TTL
        await self.redis_client.setex(auth_code, timedelta(minutes=10), user_id)
        return auth_code

    def get_login_url(self, client_id: str, redirect_uri: str, scope: str, state: str = None):
        login_url = f"/login?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
        return login_url
