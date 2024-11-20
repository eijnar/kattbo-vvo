import httpx
from logging import getLogger
from typing import Optional
from jose import JWTError, jwt
from time import time
from asyncio import Lock

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWKS_CACHE = {}
JWKS_CACHE_EXPIRY = 3600
jwks_lock = Lock()


async def get_auth0_public_keys():
    global JWKS_CACHE
    if JWKS_CACHE and JWKS_CACHE['expiry'] > time():
        cache = JWKS_CACHE['keys']
        logger.debug(f'JWKS_CACHE returning {cache}')
        return cache

    async with jwks_lock:
        if JWKS_CACHE and JWKS_CACHE['expiry'] > time():
            lock = JWKS_CACHE['keys']
            logger.debug(f'async with jwks_lock returning {lock}')
            return lock

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = response.json()
            JWKS_CACHE = {
                'keys': jwks['keys'],
                'expiry': time() + JWKS_CACHE_EXPIRY
            }
            result = jwks['keys']
            logger.debug(f'Returning fetched data: {result}')
            return result


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
