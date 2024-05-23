from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.base import get_db_session
from core.security.services.client_service import ClientService


async def get_client_service(db: AsyncSession = Depends(get_db_session)):
    return ClientService(db)
