from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserModel


async def get_user(db: AsyncSession, user_id: int):
    async with db as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalars().first()
        return user
