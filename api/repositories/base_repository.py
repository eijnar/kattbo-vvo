# core/database/repositories/base_repository.py

import logging
from typing import Generic, Type, TypeVar, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

from core.exceptions import NotFoundException, DatabaseException

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def create(self, **kwargs) -> T:
        try:
            instance = self.model(**kwargs)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)
            logger.info(
                f"Created {self.model.__name__} with ID {instance.id}.")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Failed to create {self.model.__name__}: {e}")
            raise DatabaseException(
                detail=f"Failed to create {self.model.__name__}.") from e

    async def read(self, id: int) -> T:
        try:
            instance = await self.db_session.get(self.model, id)
            if not instance:
                logger.warning(
                    f"{self.model.__name__} with ID {id} not found.")
                raise NotFoundException(
                    detail=f"{self.model.__name__} with ID {id} not found.")
            logger.debug(f"Retrieved {self.model.__name__} with ID {id}.")
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to read {self.model.__name__} with ID {id}: {e}")
            raise DatabaseException(
                detail=f"Failed to read {self.model.__name__} with ID {id}.") from e

    async def list(self, limit: int = 100, offset: int = 0) -> List[T]:
        try:
            result = await self.db_session.execute(
                select(self.model).limit(limit).offset(offset)
            )
            records = result.scalars().all()
            logger.debug(
                f"Listed {len(records)} {self.model.__name__}(s) with limit={limit} and offset={offset}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Failed to list {self.model.__name__}s: {e}")
            raise DatabaseException(
                detail=f"Failed to list {self.model.__name__}s.") from e

    async def filter(self, **kwargs) -> List[T]:
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self.db_session.execute(query)
            records = result.scalars().all()
            logger.debug(
                f"Filtered {len(records)} {self.model.__name__}(s) with criteria {kwargs}.")
            return records
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to filter {self.model.__name__}s with criteria {kwargs}: {e}")
            raise DatabaseException(
                detail=f"Failed to filter {self.model.__name__}s.") from e

    async def update(self, instance: T, **kwargs) -> T:
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)

            primary_key_column = inspect(instance).mapper.primary_key[0]
            primary_key_value = getattr(instance, primary_key_column.name)

            logger.info(
                f"Updated {self.model.__name__} with {primary_key_column.name}: {primary_key_value}.")
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to update {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(
                detail=f"Failed to update {self.model.__name__} with ID {instance.id}.") from e

    async def delete(self, instance: T):
        try:
            if hasattr(instance, 'is_active'):
                # Soft delete: Set 'is_active' to False
                setattr(instance, 'is_active', False)
                logger.info(
                    f"Soft deleted {self.model.__name__} with ID {instance.id}.")
                self.db_session.add(instance)
                await self.db_session.commit()
                await self.db_session.refresh(instance)
            else:
                # Hard delete: Remove the instance from the session
                await self.db_session.delete(instance)
                logger.info(
                    f"Hard deleted {self.model.__name__} with ID {instance.id}.")
                await self.db_session.commit()
                # Do not refresh a hard-deleted instance
        except SQLAlchemyError as e:
            action = "soft delete" if hasattr(
                instance, 'is_active') else "hard delete"
            logger.error(
                f"Failed to {action} {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(
                detail=f"Failed to {action} {self.model.__name__} with ID {instance.id}.") from e

    async def get_one(self, **kwargs) -> T:
        """
        Retrieves a single instance matching the given filter criteria.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            T: The retrieved instance.

        Raises:
            NotFoundException: If no instance matches the criteria.
            DatabaseException: If a database error occurs during retrieval.
        """
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self.db_session.execute(query)
            instance = result.scalars().first()
            if not instance:
                logger.warning(
                    f"No {self.model.__name__} found matching criteria: {kwargs}")
                raise NotFoundException(
                    detail=f"No {self.model.__name__} found matching criteria.")
            logger.debug(
                f"Retrieved {self.model.__name__} matching criteria: {kwargs}")
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to retrieve {self.model.__name__} matching criteria {kwargs}: {e}")
            raise DatabaseException(
                detail=f"Failed to retrieve {self.model.__name__} by criteria.") from e
