from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from core.security.repositories.client_repository import ClientRepository
from core.security.schemas import ClientCreate, ClientUpdate, ClientInDB

class ClientService:
    def __init__(self, db: AsyncSession):
        self.repository = ClientRepository(db)

    async def get_client(self, client_id: str) -> Optional[ClientInDB]:
        return await self.repository.get_client(client_id)

    async def get_clients(self, skip: int = 0, limit: int = 10) -> List[ClientInDB]:
        return await self.repository.get_clients(skip, limit)

    async def create_client(self, client: ClientCreate) -> ClientInDB:
        return await self.repository.create_client(client)

    async def update_client(self, client_id: str, client_update: ClientUpdate) -> Optional[ClientInDB]:
        return await self.repository.update_client(client_id, client_update)

    async def delete_client(self, client_id: str) -> bool:
        return await self.repository.delete_client(client_id)
