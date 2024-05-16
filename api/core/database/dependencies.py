from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .base import get_db
from .repositories.user_repository import UserRepository

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)