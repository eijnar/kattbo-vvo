import secrets
import hashlib
from logging import getLogger
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List

from fastapi import HTTPException, status
from passlib.context import CryptContext

from core.security.models import UserContext
from services.user_service import UserService
from core.database.models.security.api import APIKey
from core.database.models.user import User
from core.security.security_repository import SecurityRepository
from core.security.jwt import decode_and_validate_token


logger = getLogger(__name__)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=102400,
    argon2__time_cost=2,
    argon2__parallelism=8
)


class SecurityService:
    def __init__(
        self,
        security_repository: SecurityRepository,
        user_service: UserService,
    ):
        self.security_repository = security_repository
        self.user_service = user_service

    def _generate_api_key(self) -> str:
        return secrets.token_urlsafe(32)

    def _generate_api_key_identifier(self, api_key: str) -> str:
        return hashlib.sha256(api_key.encode()).hexdigest()[:16]

    def _hash_api_key(self, api_key: str) -> str:
        return pwd_context.hash(api_key)

    def _verify_api_key_with_passlib(self, provided_key: str, hashed_secret: str) -> bool:
        return pwd_context.verify(provided_key, hashed_secret)

    async def create_api_key(
        self,
        user: User,
        permissions: list,
        expires_in: timedelta = None
    ) -> Tuple[APIKey, str]:
        raw_api_key = self._generate_api_key()
        identifier = self._generate_api_key_identifier(raw_api_key)
        hashed_secret = self._hash_api_key(raw_api_key)

        expires_at = datetime.now(timezone.utc) + \
            expires_in if expires_in else None

        created_api_key = await self.security_repository.create(
            identifier=identifier,
            hashed_secret=hashed_secret,
            user_id=user.id,
            expires_at=expires_at,
            permissions=permissions
        )

        return created_api_key, raw_api_key

    async def list_api_keys(self, user: User, revoked: Optional[bool]) -> List[APIKey]:
        api_keys = await self.security_repository.list_by_user(user_id=user.id, revoked=revoked)
        return api_keys

    async def revoke_api_key(self, api_key_id: str) -> APIKey:
        api_key = await self.security_repository.get_by_id(api_key_id)
        if not api_key:
            raise HTTPException(status_code=404, detail="API Key not found")

        api_key.revoked = True
        api_key.revoked_at = datetime.now(timezone.utc)
        updated_api_key = await self.security_repository.update(api_key)
        return updated_api_key

    def _extract_permissions_from_token(self, payload: dict) -> List[str]:
        """
        Extract permissions from the token payload.
        """
        permissions = payload.get('permissions', [])
        if 'scope' in payload:
            permissions.extend(payload['scope'].split())
        # Normalize permissions
        permissions = [perm.strip().lower() for perm in permissions]
        return permissions

    # --- Authentication Methods ---

    async def authenticate_with_token(self, token: str) -> UserContext:
        """
        Authenticate user using Auth0 OAuth2 token.
        """
        payload = await decode_and_validate_token(token)
        auth0_id: Optional[str] = payload.get("sub")
        if auth0_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        user = await self.user_service.get_user_by_auth0_id(auth0_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        permissions = self._extract_permissions_from_token(payload)
        logger.debug(f"Permissions extracted from token: {permissions}")

        return UserContext(user=user, permissions=permissions)

    async def authenticate_with_api_key(self, api_key: str) -> UserContext:
        """
        Authenticate a user using an API Key.
        """
        logger.debug("authenticate_with_api_key")
        identifier = self._generate_api_key_identifier(api_key)

        api_key_record = await self.security_repository.get_by_identifier(identifier=identifier)

        if not api_key_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )

        if api_key_record.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )

        if api_key_record.expires_at and api_key_record.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key expired",
                headers={"WWW-Authenticate": "ApiKey"},
            )

        # Verify the API key against the hashed key in the database
        if not self.verify_api_key_with_passlib(api_key, api_key_record.hashed_secret):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
                headers={"WWW-Authenticate": "ApiKey"},
            )

        user = api_key_record.user
        permissions = api_key_record.permissions or []
        logger.info(f"Permissions loaded from API key: {permissions}")
        return UserContext(user=user, permissions=permissions)

    # def verify_api_key(self, provided_key: str, db_session: AsyncSession) -> Optional[User]:
    #     identifier = self.generate_api_key_identifier(provided_key)
    #     api_key_obj = self.api_key_repository.get_by_identifier(identifier)

    #     if not api_key_obj or api_key_obj.revoked:
    #         return None  # No matching API key found or it's revoked

    #     if api_key_obj.expires_at and api_key_obj.expires_at < datetime.now(timezone.utc):
    #         return None  # API key has expired

    #     if self.verify_api_key_with_passlib(provided_key, api_key_obj.hashed_secret):
    #         return api_key_obj.user  # Valid API key; return associated user

    #     return None  # Invalid API key

    # --- Event Registration Token Methods ---

    # def generate_event_registration_token(self, user: User, event_id: str, expires_in: timedelta = timedelta(hours=24)) -> str:
    #     """
    #     Generate a JWT token for event registration.
    #     """
    #     payload = {
    #         "sub": user.auth0_id,
    #         "event_id": event_id,
    #         "permissions": ["register_event"],
    #         "exp": datetime.now(timezone.utc) + expires_in
    #     }
    #     token = jwt.encode(payload, self.jwt_secret,
    #                        algorithm=self.jwt_algorithm)
    #     return token

    # async def authenticate_event_registration_token(self, token: str, db_session: AsyncSession) -> User:
    #     """
    #     Authenticate user using an event registration token.
    #     """
    #     try:
    #         payload = jwt.decode(token, self.jwt_secret,
    #                              algorithms=[self.jwt_algorithm])
    #         auth0_id = payload.get("sub")
    #         event_id = payload.get("event_id")
    #         permissions = payload.get("permissions", [])

    #         if not auth0_id or not event_id:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    #         if "register_event" not in permissions:
    #             raise HTTPException(
    #                 status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    #         user = self.api_key_repository.get_user_by_auth0_id(db, auth0_id)
    #         if user is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #         if user.disabled:
    #             raise HTTPException(
    #                 status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    #         return user

    #     except JWTError:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
