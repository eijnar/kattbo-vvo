from logging import getLogger
from typing import list, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from repositories.base_repository import BaseRepository
from core.database.models import HuntingYearTask


logger = getLogger(__name__)

class HuntingYearTaskRepository(BaseRepository[HuntingYearTask]):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(HuntingYearTask, db_session)
