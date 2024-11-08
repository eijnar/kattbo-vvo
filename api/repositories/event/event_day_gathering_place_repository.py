from sqlalchemy.ext.asyncio import AsyncSession

from repositories.base_repository import BaseRepository
from core.database.models import EventDayGatheringPlace


class EventDayGatheringRepository(BaseRepository[EventDayGatheringPlace]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(EventDayGatheringPlace, db_session)
