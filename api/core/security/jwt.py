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

async def get_auth0_public_key():
    global JWKS_CACHE
    if JWKS_CACHE and JWKS_CACHE['expiry'] > time():
        logger.debug(f'JWKS_CACHE returning {JWKS_CACHE['keys']}')
        return JWKS_CACHE['keys']
    
    async with jwks_lock:
        if JWKS_CACHE and JWKS_CACHE['expiry'] > time():
            logger.debug(f'async with jwks_lock returning {JWKS_CACHE['keys']}')
            return JWKS_CACHE['keys']
        
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get("https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = await response.json()
            JWKS_CACHE = {
                'keys': jwks['keys'],
                'expiry': time() + JWKS_CACHE_EXPIRY
            }
            logger.debug(f'Returning fetched data: {jwks['keys']}')
            return jwks['keys']
        
        #jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        #response = requests.get(jwks_url, timeout=5.0)
    #     if response.status_code != 200:
    #         raise HTTPException(
    #             status_code=500, detail="Failed to fetch public keys")
    # return response.json()


async def decode_jwt(token: str):
    jwks = await get_auth0_public_key()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks['keys']:
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