import requests
from jose import JWTError, jwt
from fastapi import HTTPException

from core.config import settings


def get_public_key():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
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
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=settings.ALGORITHMS,
            audience=settings.API_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

