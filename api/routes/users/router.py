from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.logger import logger
from core.database import get_db
from models.user import UserModel
from schemas.user.user import UserSchema

users = APIRouter(prefix="/users")

@users.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        async with db:
            query = select(UserModel)
            result = await db.execute(query)
            users = result.scalars().all()
            return users
    except Exception as e:    
        raise HTTPException(status_code=500, detail=f"failed... {e}")
    
@users.post("/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = UserModel(**user.dict())
    
    try:    
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to add user"
        )