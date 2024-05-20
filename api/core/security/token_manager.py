import logging
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import Depends
from redis import Redis
from fastapi import HTTPException, status
from jose import jwt

from core.config import settings
from core.security.redis_client import get_redis_client_for_tokens, get_redis_client_for_unconfirmed_users


logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self, redis):
        self.redis = redis

    @classmethod
    async def create(cls, redis):
        return cls(redis)

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

        # assert 'sub' in data, "Subject (sub) must be provided in the token data."

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

    async def create_token(self, user_id, token_type, scopes=None, expires_delta=1, version_ttl=None ):
        version = await self._get_user_version(user_id, version_ttl)
        data = {"sub": str(user_id), }
        if scopes:
            data["scopes"] = scopes

        token_key = f"{token_type}_token:{user_id}:{uuid4()}"
        token = self._create_token(
            data, expires_delta, version, token_type)
        await self.redis.setex(token_key, int(expires_delta.total_seconds()), token)
        return token

    async def validate_token_version(self, user_id, token_version):
        """
        Validate the token version for a user.
        Parameters:
            user_id: The ID of the user.
            token_version: The version of the token to validate.
        Returns:
            bool: True if the token version is valid, False otherwise.
        """
        current_version = await self.redis.get(f"user_version:{user_id}")
        if not current_version or int(current_version) != int(token_version):
            return False
        return True

    async def validate_token(self, token):
        """
        Validates a JWT token by decoding it and checking the stored version against the payload version.

        Parameters:
            token (str): The JWT token to validate.

        Returns:
            dict: The decoded payload of the token if valid.

        Raises:
            HTTPException: If the token version mismatches or the token is invalid.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            stored_version = await self._get_user_version(payload['sub'])
            if payload['ver'] != stored_version:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token version mismatch",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload
        except jwt.JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def _get_user_version(self, user_id, version_ttl=None):
        version_key = f"user_version:{str(user_id)}"
        version = await self.redis.get(version_key)
        if version is None:
            await self.redis.set(version_key, 1)
            if version_ttl:
                await self.redis.expire(version_key, int(version_ttl.total_seconds()))
            return 1
        return int(version)

    async def _increment_user_version(self, user_id):
        version_key = f"user_version:{str(user_id)}"
        await self.redis.incr(version_key)

    async def invalidate_tokens(self, user_id, token_type="access"):
        keys = await self.redis.keys(f"{token_type}_token:{user_id}:*")
        for key in keys:
            await self.redis.delete(key)

    async def invalidate_all_tokens_for_user(self, user_id):
        logger.info(f"Invalidating all tokens for user ID {user_id}.")
        await self.invalidate_tokens(user_id, token_type="access")
        await self.invalidate_tokens(user_id, token_type="refresh")
        await self.invalidate_tokens(user_id, token_type="password_reset")

async def get_token_manager(redis: Redis = Depends(get_redis_client_for_tokens)) -> TokenManager:
    return await TokenManager.create(redis)

async def get_token_manager_for_unconfirmed_users(redis: Redis = Depends(get_redis_client_for_unconfirmed_users)) -> TokenManager:
    return await TokenManager.create(redis)
