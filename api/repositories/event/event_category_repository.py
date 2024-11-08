from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import EventCategory


class EventCategoryRepository(BaseRepository[EventCategory]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(EventCategory, db_session)
