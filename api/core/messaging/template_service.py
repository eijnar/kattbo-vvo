from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database.models import Template

class TemplateService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_template(self, service: str, name: str):
        result = await self.db_session.execute(
            select(Template).filter_by(service=service, name=name)
        )
        return result.scalars().first()