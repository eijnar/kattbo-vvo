import requests
from logging import getLogger
from typing import Optional
from jose import JWTError, jwt

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

logger = getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_public_key():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url, timeout=5.0)
    if response.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Failed to fetch public keys")
    return response.json()


def decode_jwt(token: str):
    jwks = get_public_key()
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
        # Decode the token without verifying the signature to extract claims
        unverified_payload = jwt.decode(
            token,
            key=None,
            algorithms=settings.ALGORITHMS,
            options={"verify_signature": False}
        )

        # Extract the 'aud' claim and ensure it's a list
        logger.debug(f"Unverified_payload: {unverified_payload}")
        token_audience = unverified_payload.get('aud')
        if isinstance(token_audience, str):
            token_audience = [token_audience]

        # Verify that the expected audience is in the token's 'aud' claim
        expected_audience = settings.API_AUDIENCE
        if expected_audience not in token_audience:
            raise JWTError('Invalid audience')

        # Now decode the token with signature verification, skipping audience check
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
        payload = decode_jwt(token)
        logger.debug(f"Decoded payload: {payload}")
        return payload
    except JWTError as e:
        logger.warning(f"Token decode failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )