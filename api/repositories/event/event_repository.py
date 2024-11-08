from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import Event


class EventRepository(BaseRepository[Event]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(Event, db_session)
