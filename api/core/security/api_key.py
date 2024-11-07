from datetime import datetime, timezone

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext

from core.database.models.security.api import APIKey
from core.database.models.user import User
from core.dependencies import get_db_session


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=102400,   # 100 MiB
    argon2__time_cost=2,
    argon2__parallelism=8
)


def generate_api_key() -> str:
    # Generates a 43-character URL-safe string
    return secrets.token_urlsafe(32)


def generate_api_key_identifier(api_key: str) -> str:
    # Using SHA-256 to create a deterministic identifier
    # 16-character identifier
    return hashlib.sha256(api_key.encode()).hexdigest()[:16]


def hash_api_key(api_key: str) -> str:
    return pwd_context.hash(api_key)


def verify_api_key_with_passlib(provided_key: str, hashed_secret: str) -> bool:
    return pwd_context.verify(provided_key, hashed_secret)


def create_api_key(db: get_db_session, user: User, permissions: list, expires_in: timedelta = None) -> APIKey:
    raw_api_key = generate_api_key()
    identifier = generate_api_key_identifier(raw_api_key)
    hashed_secret = hash_api_key(raw_api_key)

    api_key = APIKey(
        identifier=identifier,
        hashed_secret=hashed_secret,
        user_id=user.id,
        permissions=permissions,
        expires_at=datetime.now(timezone.utc) +
        expires_in if expires_in else None
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key, raw_api_key  # Return both; raw_api_key shown only once


def verify_api_key(provided_key: str, db: get_db_session) -> Optional[User]:
    identifier = generate_api_key_identifier(provided_key)
    api_key_obj = db.query(APIKey).filter(
        APIKey.identifier == identifier, APIKey.revoked == False).first()

    if not api_key_obj:
        return None  # No matching API key found

    if verify_api_key_with_passlib(provided_key, api_key_obj.hashed_secret):
        if api_key_obj.expires_at and api_key_obj.expires_at < datetime.now(timezone.utc):
            return None  # API key has expired
        return api_key_obj.user  # Valid API key

    return None  # Invalid API key
