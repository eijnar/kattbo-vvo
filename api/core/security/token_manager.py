from uuid import uuid4
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt, JWTError

from core.config import settings
from core.logger import logger
from .redis_client import get_redis_client


class TokenManager:
    def __init__(self, redis):
        self.redis = redis

    @staticmethod
    def _create_token(data, expires_delta, version, token_type):
        """
        Create a JWT token with specified data, expiry, version, and type.

        Parameters:
        data (dict): The payload data for the token.
        expires_delta (timedelta): How long until the token expires.
        version (int): The version number of the token.
        token_type (str): The type of the token (e.g., 'access', 'refresh', 'reset').

        Returns:
        str: A JWT token as a string.
        """

        assert 'sub' in data, "Subject (sub) must be provided in the token data."

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({
            "exp": expire,
            "ver": version,
            "type": token_type
        })
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    async def create_access_token(self, user_id, scopes, expires_delta=timedelta(minutes=15)):
        version = await self._get_user_version(user_id)
        data = {"sub": str(user_id), "scopes": scopes, "ver": version}
        access_token = self._create_token(
            data, expires_delta, version, token_type="access")
        token_key = f"access_token:{user_id}:{uuid4()}"
        await self.redis.setex(token_key, int(expires_delta.total_seconds()), access_token)
        return access_token

    async def create_refresh_token(self, user_id, expires_delta=timedelta(days=7)):
        version = await self._get_user_version(user_id)
        data = {"sub": str(user_id)}
        refresh_token = self._create_token(
            data, expires_delta, version, token_type="refresh")
        token_key = f"refresh_token:{user_id}:{uuid4()}"
        await self.redis.setex(token_key, int(expires_delta.total_seconds()), refresh_token)
        return refresh_token

    async def create_password_reset_token(self, user_id, version):
        """
        Generate a password reset token for a given user.

        Parameters:
        user_id (int): The user ID for whom to generate the token.
        version (int): The current version number for token invalidation.

        Returns:
        str: A JWT token specifically for password reset.
        """
        data = {
            "sub": str(user_id),
            "scope": ["reset_token"]
        }

        expires_delta = timedelta(minutes=settings.RESET_TOKEN_LIFESPAN_MINUTE)
        token_type = "reset"

        return self._create_token(data, expires_delta, version, token_type)

    async def validate_token_version(self, user_id, token_version):
        if self.redis is None:
            logger.error(
                "Error: Attempting to use Redis client before it is initialized.")
        current_version = await self.redis.get(f"user_version:{user_id}")
        if not current_version or int(current_version) != int(token_version):
            return False
        return True

    async def validate_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            stored_version = await self._get_user_version(payload['sub'])
            if payload['ver'] != stored_version:
                print(
                    f"Version mismatch: token version {payload['ver']} vs stored version {stored_version}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token version mismatch",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload
        except jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token due to {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def _get_user_version(self, user_id):
        version_key = f"user_version:{str(user_id)}"
        version = await self.redis.get(version_key)
        if version is None:
            await self.redis.set(version_key, 1)
            return 1
        return int(version)

    async def _increment_user_version(self, user_id):
        version_key = f"user_version:{str(user_id)}"
        await self.redis.incr(version_key)

    async def invalidate_access_tokens(self, user_id):
        keys = await self.redis.keys(f"access_token:*{user_id}:*")
        for key in keys:
            await self.redis.delete(key)

    async def invalidate_refresh_tokens(self, user_id):
        keys = await self.redis.keys(f"refresh_token:{user_id}:*")
        for key in keys:
            await self.redis.delete(key)

    @classmethod
    async def create(cls):
        redis = await get_redis_client()
        return cls(redis)


async def get_token_manager() -> TokenManager:
    return await TokenManager.create()
