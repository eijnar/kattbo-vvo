from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

class CRUDMixin:
    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        instance = cls(**kwargs)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    @classmethod
    async def read(cls, db: AsyncSession, id: int):
        return await db.get(cls, id)

    async def update(self, db: AsyncSession, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.commit()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession):
        await db.delete(self)
        await db.commit()