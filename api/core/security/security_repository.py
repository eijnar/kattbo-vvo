from logging import getLogger
from uuid import UUID

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from repositories.base_repository import BaseRepository
from core.database.models.security.api import APIKey
from core.database.models.user import User
from core.exceptions import DatabaseError


logger = getLogger(__name__)

class SecurityRepository(BaseRepository[APIKey]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(APIKey, db_session)
        self.db_session = db_session

    async def get_by_id(self, id: UUID) -> Optional[APIKey]:
        query = select(self.model).filter(self.model.id == id)
        result = await self.db_session.execute(query)
        return result.scalars().first()

    async def get_by_identifier(self, identifier: str) -> Optional[APIKey]:
        try:
            query = (
                select(self.model)
                .options(selectinload(self.model.user))
                .filter(self.model.identifier == identifier)
            )
            result = await self.db_session.execute(query)
            api_key = result.scalars().first()
            return api_key
        except SQLAlchemyError as e:
            logger.error(f"Failed to fetch API key by identifier {identifier}: {e}")
            raise DatabaseError(detail="Failed to fetch API key.") from e

    async def list_by_user(self, user_id: str, revoked: Optional[bool] = None) -> List[APIKey]:
        try:
            query = select(self.model).filter(self.model.user_id == user_id)
            if revoked is not None:
                query = query.filter(self.model.revoked == revoked)
            # If revoked is None, do not filter by revoked status (return all)
            result = await self.db_session.execute(query)
            api_keys = result.scalars().all()
            return api_keys
        except SQLAlchemyError as e:
            logger.error(f"Failed to list API keys for user {user_id}: {e}")
            raise DatabaseError(detail="Failed to list API keys.") from e

    async def revoke_api_key(self, api_key: APIKey) -> APIKey:
        try:
            api_key.revoked = True
            await self.db_session.commit()
            await self.db_session.refresh(api_key)
            return api_key
        except SQLAlchemyError as e:
            logger.error(f"Failed to revoke API key {api_key.identifier}: {e}")
            raise DatabaseError(detail="Failed to revoke API key.") from e

    async def get_user_by_auth0_id(self, auth0_id: str) -> Optional[User]:
        result = await self.db_session.execute(select(User).filter(User.auth0_id == auth0_id))
        return result.scalars().first()

