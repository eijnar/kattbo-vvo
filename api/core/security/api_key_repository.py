# core/database/repositories/api_key_repository.py

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database.models.mixins import CRUDMixin
from core.database.models.security import APIKeyModel
from core.database.models.user import UserModel

class APIKeyRepository(CRUDMixin[APIKeyModel]):
    model = APIKeyModel
    
    def __init__(self, db: AsyncSession):
        super().__init__(APIKeyModel, db)

    async def get_by_identifier(self, identifier: str) -> Optional[APIKeyModel]:
        result = await self.db.execute(select(self.model).filter(self.model.identifier == identifier))
        return result.scalars().first()

    async def list_by_user(self, user_id: str) -> List[APIKeyModel]:
        result = await self.db.execute(select(self.model).filter(self.model.user_id == user_id))
        return result.scalars().all()

    async def revoke_api_key(self, api_key: APIKeyModel) -> APIKeyModel:
        api_key.revoked = True
        await self.db.commit()
        await self.db.refresh(api_key)
        return api_key

    async def get_user_by_auth0_id(self, auth0_id: str) -> Optional[UserModel]:
        result = await self.db.execute(select(UserModel).filter(UserModel.auth0_id == auth0_id))
        return result.scalars().first()
