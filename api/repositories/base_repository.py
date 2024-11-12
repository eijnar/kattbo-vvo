# core/database/repositories/base_repository.py

import logging
from typing import Generic, Type, TypeVar, List, Optional, Any

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
            logger.debug(
                "Create new instance",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": kwargs.get('id', 'unknown'),
                    "data": kwargs
                }
            )
            instance = self.model(**kwargs)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)
            logger.info(
                f"Created new instance",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": str(instance.id)
                })
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Failed to create {self.model.__name__}: {e}")
            raise DatabaseException(
                detail=f"Failed to create {self.model.__name__}.") from e

    async def read(self, id: int, raise_if_not_found: bool = True) -> T:
        try:
            logger.debug(
                "Reading instance",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": str(id)
                }
            )
            instance = await self.db_session.get(self.model, id)
            if not instance:
                logger.debug(
                    f"{self.model.__name__} with ID {id} not found",
                    extra={"resource.type": self.model.__name__,
                           "resource.id": str(id)}
                )
                if raise_if_not_found:
                    raise NotFoundException(
                        detail=f"{self.model.__name__} with ID {id} not found.")
            logger.debug(
                "Retrieved instance",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": str(id)
                }
            )
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to read {self.model.__name__} with ID {id}: {e}")
            raise DatabaseException(
                detail=f"Failed to read {self.model.__name__} with ID {id}.") from e

    async def list(
        self, 
        limit: int = 100, 
        offset: int = 0,
        raise_if_not_found: bool = False
    ) -> List[T]:
        try:
            logger.debug(
                "Listing instances",
                extra={
                    "resource.type": self.model.__name__,
                    "limit": limit,
                    "offset": offset
                }
            )
            query = select(self.model).where(
                getattr(self.model, 'is_active', True) == True).limit(limit).offset(offset)

            result = await self.db_session.execute(query)
            records = result.scalars().all()
            if records:
                logger.info(
                    f"Listed {len(records)} {self.model.__name__}(s)",
                    extra={
                        "resource.type": self.model.__name__,
                        "count": len(records)
                    }
                )
            else: 
                logger.info(
                    f"No {self.model.__name__} records found",
                    extra={
                        "resource.type": self.model.__name__,
                        "count": 0
                    }
                )
                if raise_if_not_found:
                    NotFoundException(detail="No records found")
                    
            return records

        except SQLAlchemyError as e:
            logger.error(f"Failed to list {self.model.__name__}s: {e}")
            raise DatabaseException(
                detail=f"Failed to list {self.model.__name__}s."
            ) from e

    async def filter(self, raise_if_not_found: bool = False, order_by: Optional[List[Any]] = None, **kwargs) -> List[T]:
        try:
            logger.debug(
                "Filtering instances",
                extra={
                    "resource.type": self.model.__name__,
                    "criteria": kwargs
                }
            )
            
            query = select(self.model).filter_by(**kwargs)
            
            if order_by:
                query = query.order_by(order_by)
                
            result = await self.db_session.execute(query)
            records = result.scalars().all()
            if not records:
                logger.debug(
                    f"No {self.model.__name__}s found with criteria {kwargs}",
                    extra={
                        "resource.type": self.model.__name__,
                        "criteria": kwargs
                    }
                )
                
                if raise_if_not_found:
                    raise NotFoundException(
                        detail=f"No {self.model.__name__}s found with criteria {kwargs}."
                    )

            logger.info(
                f"Filtered {len(records)} {self.model.__name__}(s)",
                extra={
                    "resource.type": self.model.__name__,
                    "count": len(records),
                    "criteria": kwargs
                }
            )
            return records

        except SQLAlchemyError as e:
            logger.error(
                f"Failed to filter {self.model.__name__}s with criteria {kwargs}: {e}")
            raise DatabaseException(
                detail=f"Failed to filter {self.model.__name__}s.") from e

    async def update(self, instance: T, **kwargs) -> T:
        try:
            logger.debug(
                "Updating instance",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": str(instance.id),
                    "update_fields": kwargs
                }
            )
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db_session.add(instance)
            await self.db_session.commit()
            await self.db_session.refresh(instance)

            primary_key_column = inspect(instance).mapper.primary_key[0]
            primary_key_value = getattr(instance, primary_key_column.name)

            logger.info(
                f"Updated {self.model.__name__} with {primary_key_column.name}: {primary_key_value}.",
                extra={
                    "resource.type": self.model.__name__,
                    "resource.id": str(primary_key_value),
                    "update_fields": kwargs
                }
            )
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to update {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(
                detail=f"Failed to update {self.model.__name__} with ID {instance.id}.") from e

    async def delete(self, instance: T):
        try:
            if hasattr(instance, 'is_active'):
                logger.debug(
                    "Soft deleting instance",
                    extra={
                        "resource.type": self.model.__name__,
                        "resource.id": str(instance.id)
                    }
                )
                setattr(instance, 'is_active', False)
                logger.info(
                    f"Soft deleted {self.model.__name__} with ID {instance.id}.",
                    extra={
                        "resource.type": self.model.__name__,
                        "resource.id": str(instance.id)
                    }
                )
                self.db_session.add(instance)
                await self.db_session.commit()
                await self.db_session.refresh(instance)
            else:
                logger.debug(
                    "Hard deleting instance",
                    extra={
                        "resource.type": self.model.__name__,
                        "resource.id": str(instance.id)
                    }
                )
                await self.db_session.delete(instance)
                logger.info(
                    f"Hard deleted {self.model.__name__} with ID {instance.id}.")
                await self.db_session.commit()
                logger.info(
                    f"Hard deleted {self.model.__name__} with ID {instance.id}.",
                    extra={
                        "resource.type": self.model.__name__,
                        "resource.id": instance.id
                    }
                )

        except SQLAlchemyError as e:
            action = "soft delete" if hasattr(
                instance, 'is_active') else "hard delete"
            logger.error(
                f"Failed to {action} {self.model.__name__} with ID {instance.id}: {e}")
            raise DatabaseException(
                detail=f"Failed to {action} {self.model.__name__} with ID {instance.id}.") from e

    async def get_one(self, **kwargs) -> T:
        try:
            logger.debug(
                "Fetching one instance based on criteria",
                extra={
                    "resource.type": self.model.__name__,
                    "criteria": kwargs
                }
            )
            query = select(self.model).filter_by(**kwargs)
            result = await self.db_session.execute(query)
            instance = result.scalars().first()
            if not instance:
                logger.debug(
                    f"No {self.model.__name__} found with criteria {kwargs}",
                    extra={
                        "resource.type": self.model.__name__,
                        "criteria": kwargs
                    }
                )
            logger.debug(
                "Retrieved instance",
                extra={
                    "resource.type": self.model.__name__,
                    "criteria": kwargs,
                    "resource.id": str(instance.id)
                }
            )
            return instance
        except SQLAlchemyError as e:
            logger.error(
                f"Failed to retrieve {self.model.__name__} matching criteria {kwargs}: {e}")
            raise DatabaseException(
                detail=f"Failed to retrieve {self.model.__name__} by criteria.") from e

    async def exists(self, **kwargs) -> bool:
        try:
            logger.debug(
                "Checking existence of instance",
                extra={
                    "resource.type": self.model.__name__,
                    "criteria": kwargs
                }
            )
            query = select(self.model).filter_by(**kwargs).limit(1)
            result = await self.db_session.execute(query)
            record = result.scalars().first()
            exists = record is not None
            logger.debug(
                "Existence check result",
                extra={
                    "resource.type": self.model.__name__,
                    "criteria": kwargs,
                    "exists": exists
                }
            )
            return exists

        except SQLAlchemyError as e:
            raise DatabaseException(
                detail=f"Failed to verify existence of {self.model.__name__} with criteria {kwargs}: {e}",
                extra={"criteria": kwargs, "error": str(e)}
            ) from e
