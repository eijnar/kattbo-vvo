from datetime import datetime, timedelta, timezone
from typing import Union, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt

from core.config import settings
from core.database import get_db
from models.user import ScopeModel, RoleModel, UserModel


async def get_scopes(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ScopeModel))
        scopes = result.scalars().all()
        return {scope.scope: scope.description for scope in scopes}
    except Exception:
        print("sk")


async def get_user_scopes(user_id: int, db: AsyncSession) -> list:
    query = select(ScopeModel.scope).join(ScopeModel.roles).join(
        RoleModel.users).where(UserModel.id == user_id)
    result = await db.execute(query)
    scopes = result.scalars().all()
    return scopes
