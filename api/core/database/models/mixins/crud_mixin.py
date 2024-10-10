from logging import getLogger
from typing import Type, TypeVar, List, Optional, Generic

from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.exceptions import NotFoundException, DatabaseException

T = TypeVar('T')
logger = getLogger(__name__)


class CRUDMixin(Generic[T]):
    model: Type[T]

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, **kwargs) -> T:
        """
        Create a new record in the database.
        """
        try:
            instance = self.model(**kwargs)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)
            logger.info(f"Created {self.model.__name__} with ID {instance.id}.")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Failed to create {self.model.__name__}: {e}")
            raise DatabaseException(detail=f"Failed to create {self.model.__name__}.") from e

    async def read(self, id: int) -> Optional[T]:
        """
        Read a record by its ID.
        """
        try:
            result = await self.db_session.get(self.model, id)
            if not result:
                logger.warning(f"{self.model.__name__} with ID {id} not found.")
                raise NotFoundException(detail=f"{self.model.__name__} with ID {id} not found.")
            logger.info(f"Retrieved {self.model.__name__} with ID {id}.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Failed to read {self.model.__name__} with ID {id}: {e}")
            raise DatabaseException(detail=f"Failed to read {self.model.__name__} with ID {id}.") from e

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        """
        List records with pagination.
        """
        try:
            result = await self.db_session.execute(
                select(self.model).limit(limit).offset(offset)
            )
            records = result.scalars().all()
            logger.info(f"Listed {len(records)} {self.model.__name__}(s) with limit={limit} and offset={offset}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Failed to list {self.model.__name__}s: {e}")
            raise DatabaseException(detail=f"Failed to list {self.model.__name__}s.") from e

    async def filter(self, **kwargs) -> List[T]:
        """
        Filter records based on provided criteria.
        """
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self.db_session.execute(query)
            records = result.scalars().all()
            logger.info(f"Filtered {len(records)} {self.model.__name__}(s) with criteria {kwargs}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Failed to filter {self.model.__name__}s with criteria {kwargs}: {e}")
            raise DatabaseException(detail=f"Failed to filter {self.model.__name__}s.") from e

    async def update(self, instance: T, **kwargs) -> T:
        """
        Update a record with new values.
        """
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)
            logger.info(f"Updated {self.model.__name__} with ID {instance.id}.")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Failed to update {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(detail=f"Failed to update {self.model.__name__} with ID {instance.id}.") from e

    async def delete(self, instance: T):
        """
        Soft delete a record by setting 'is_active' to False.
        """
        try:
            if hasattr(instance, 'is_active'):
                setattr(instance, 'is_active', False)
                logger.info(f"Soft deleted {self.model.__name__} with ID {instance.id}.")
            else:
                await self.db_session.delete(instance)
                logger.info(f"Hard deleted {self.model.__name__} with ID {instance.id}.")
            self.db_session.add(instance) if hasattr(instance, 'is_active') else None
            await self.db_session.commit()
            await self.db_session.refresh(instance)
        except SQLAlchemyError as e:
            action = "soft delete" if hasattr(instance, 'is_active') else "hard delete"
            logger.error(f"Failed to {action} {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(detail=f"Failed to {action} {self.model.__name__} with ID {instance.id}.") from e
