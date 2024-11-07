import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from core.database.models.security.api import APIKeyModel
from core.database.models.user import UserModel
from core.security.security_repository import APIKeyRepository
from core.security.jwt import decode_and_validate_token

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=102400,
    argon2__time_cost=2,
    argon2__parallelism=8
)

class SecurityService:
    def __init__(self, api_key_repository: APIKeyRepository, jwt_secret: str, jwt_algorithm: str = "HS256"):
        self.api_key_repository = api_key_repository
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    # --- API Key Management Methods ---
    def generate_api_key(self) -> str:
        return secrets.token_urlsafe(32)  # Generates a 43-character URL-safe string

    def generate_api_key_identifier(self, api_key: str) -> str:
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]  # 16-character identifier

    def hash_api_key(self, api_key: str) -> str:
        return pwd_context.hash(api_key)

    def verify_api_key_with_passlib(self, provided_key: str, hashed_key: str) -> bool:
        return pwd_context.verify(provided_key, hashed_key)

    def create_api_key(
        self, user: UserModel, permissions: list, expires_in: timedelta = None
    ) -> Tuple[APIKeyModel, str]:
        raw_api_key = self.generate_api_key()
        identifier = self.generate_api_key_identifier(raw_api_key)
        hashed_key = self.hash_api_key(raw_api_key)

        api_key = APIKeyModel(
            identifier=identifier,
            hashed_key=hashed_key,
            user_id=user.id,
            permissions=permissions,
            expires_at=datetime.utcnow() + expires_in if expires_in else None
        )

        created_api_key = self.api_key_repository.create(api_key)
        return created_api_key, raw_api_key

    def list_api_keys(self, user: UserModel, db: Session) -> list:
        return self.api_key_repository.list_by_user(db, user_id=user.id)

    def revoke_api_key(self, api_key: APIKeyModel, db: Session) -> APIKeyModel:
        return self.api_key_repository.revoke_api_key(api_key)

    # --- Authentication Methods ---

    async def authenticate_with_token(self, token: str, db: Session) -> UserModel:
        """
        Authenticate user using Auth0 OAuth2 token.
        """
        payload = decode_and_validate_token(token)
        auth0_id: str = payload.get("sub")
        if auth0_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        user = self.api_key_repository.get_user_by_auth0_id(db, auth0_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    def authenticate_with_api_key(self, api_key: str, db: Session) -> UserModel:
        """
        Authenticate user using API Key.
        """
        user = self.verify_api_key(provided_key=api_key, db=db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        return user

    def verify_api_key(self, provided_key: str, db: Session) -> Optional[UserModel]:
        identifier = self.generate_api_key_identifier(provided_key)
        api_key_obj = self.api_key_repository.get_by_identifier(db, identifier)

        if not api_key_obj or api_key_obj.revoked:
            return None  # No matching API key found or it's revoked

        if api_key_obj.expires_at and api_key_obj.expires_at < datetime.utcnow():
            return None  # API key has expired

        if self.verify_api_key_with_passlib(provided_key, api_key_obj.hashed_key):
            return api_key_obj.user  # Valid API key; return associated user

        return None  # Invalid API key

    # --- Event Registration Token Methods ---

    def generate_event_registration_token(self, user: UserModel, event_id: str, expires_in: timedelta = timedelta(hours=24)) -> str:
        """
        Generate a JWT token for event registration.
        """
        payload = {
            "sub": user.auth0_id,
            "event_id": event_id,
            "permissions": ["register_event"],
            "exp": datetime.utcnow() + expires_in
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token

    async def authenticate_event_registration_token(self, token: str, db: Session) -> UserModel:
        """
        Authenticate user using an event registration token.
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            auth0_id = payload.get("sub")
            event_id = payload.get("event_id")
            permissions = payload.get("permissions", [])

            if not auth0_id or not event_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            if "register_event" not in permissions:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

            user = self.api_key_repository.get_user_by_auth0_id(db, auth0_id)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if user.disabled:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

            return user

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
