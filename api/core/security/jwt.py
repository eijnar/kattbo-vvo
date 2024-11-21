import httpx
import json
from logging import getLogger
from typing import Optional
from jose import JWTError, jwt
from time import time

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from redis import asyncio as aioredis
from asyncio import Lock

from core.config import settings
from core.redis.client import get_redis_client_for_cache

logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWKS_CACHE = {}
JWKS_CACHE_EXPIRY = 3600
jwks_lock = Lock()


async def get_auth0_public_keys(redis: aioredis = Depends(get_redis_client_for_cache)):
    cache_key = "cache:auth0:jwks"

    cached_data = await redis.get(cache_key)
    if cached_data:
        jwks = json.loads(cached_data)
        logger.debug(f'Cache returning data from Redis: {jwks}')
        return jwks['keys']

    async with jwks_lock:
        cached_data = await redis.get(cache_key)
        if cached_data:
            jwks = json.loads(cached_data)
            return jwks['keys']

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = response.json()
            await redis.set(
                cache_key,
                json.dumps(jwks),
                ex=JWKS_CACHE_EXPIRY
            )
            return jwks['keys']


async def decode_jwt(token: str):
    jwks_keys = await get_auth0_public_keys()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks_keys:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if not rsa_key:
        raise HTTPException(
            status_code=401, detail="Unable to find appropriate key")
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=settings.ALGORITHMS,
            options={"verify_aud": False},
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )

        return payload
    except JWTError as e:
        logger.error(f"Failure to decode token: {e}")
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


async def decode_and_validate_token(
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[dict]:
    if not token:
        logger.debug("No token provided for decoding.")
        return None
    try:
        logger.debug(token)
        payload = await decode_jwt(token)
        logger.debug(f"Decoded payload: {payload}")
        return payload
    except JWTError as e:
        logger.warning(f"Token decode failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
