from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserModel  # Assuming your user model is named User and imported properly

async def fetch_user_by_email(db: AsyncSession, email: str):
    async with db as session:
        result = await session.execute(select(UserModel).filter(UserModel.email == email))
        user = result.scalars().first()
        return user