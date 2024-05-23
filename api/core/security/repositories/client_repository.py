from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from core.security.models.client import ClientModel
from core.security.schemas import ClientCreate, ClientUpdate

class ClientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_client(self, client_id: str) -> Optional[ClientModel]:
        stmt = select(ClientModel).filter(ClientModel.client_id == client_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_clients(self, skip: int = 0, limit: int = 10) -> List[ClientModel]:
        stmt = select(ClientModel).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_client(self, client: ClientCreate) -> ClientModel:
        db_client = ClientModel(**client.dict())
        self.db.add(db_client)
        await self.db.commit()
        await self.db.refresh(db_client)
        return db_client

    async def update_client(self, client_id: str, client_update: ClientUpdate) -> Optional[ClientModel]:
        db_client = await self.get_client(client_id)
        if db_client:
            update_data = client_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_client, key, value)
            await self.db.commit()
            await self.db.refresh(db_client)
        return db_client

    async def delete_client(self, client_id: str) -> bool:
        db_client = await self.get_client(client_id)
        if db_client:
            await self.db.delete(db_client)
            await self.db.commit()
            return True
        return False
