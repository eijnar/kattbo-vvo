from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import EventDay


class EventDayRepository(BaseRepository[EventDay]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(EventDay, db_session)
