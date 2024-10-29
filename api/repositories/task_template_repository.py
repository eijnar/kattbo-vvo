from logging import getLogger
from typing import list, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from repositories.base_repository import BaseRepository
from core.database.models import TaskTemplate


logger = getLogger(__name__)

class TaskTemplateRepository(BaseRepository[TaskTemplate]):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(TaskTemplate, db_session)
        
    