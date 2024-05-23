import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas import UserCreateSchema
from core.security.api_key import get_api_key
from core.database.models import UserModel
from core.database.base import get_db_session


logger = logging.getLogger(__name__)

router = APIRouter(tags=["user"])


@router.post("/register")
async def register_user(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db_session),

):
    logging.info(f"Received registration request with user data: {user}")
    result = await db.execute(
        select(UserModel).filter(UserModel.auth0_id == user.auth0_id)
    )
    db_user = result.scalars().first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    new_user = UserModel(
        auth0_id=user.auth0_id,
        email=user.email,
        first_name=user.first_name,
        disabled=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
