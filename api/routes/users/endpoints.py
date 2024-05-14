from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from core.logger import logger
from core.database import get_db
from core.security import get_password_hash, get_current_active_user, UserBaseSchema
from core.security.token_manager import TokenManager, get_token_manager
from models.user import UserModel
from .crud import fetch_user_by_email

users = APIRouter(prefix="/users")

@users.post("/password-reset-request")
async def request_password_reset(
    email: str,
    db: AsyncSession = Depends(get_db),
    token_manager: TokenManager = Depends(get_token_manager)
):
    user = await fetch_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_version = await token_manager._get_user_version(user.id)
    
    reset_token = await token_manager.create_password_reset_token(user.id, current_version)
    logger.debug(f"Sending reset email to {user.id}. Current version {current_version}. Reset token: {reset_token}")

@users.get("/", response_model=List[UserBaseSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        async with db:

            query = select(UserModel)
            result = await db.execute(query)
            users = result.scalars().all()
            return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed... {e}")


@users.get("/current", response_model=UserBaseSchema)
async def read_users_me(
    current_user: UserModel = Security(
        get_current_active_user, scopes=["users:read"])
):
    return current_user


@users.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    phone_number: str,
    current_user: UserModel = Security(
        get_current_active_user, scopes=["users:post"]),
    db: AsyncSession = Depends(get_db)
):
    hashed_password = get_password_hash(password)
    new_user = UserModel(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"email": new_user.email, "message": "User created successfully"}
