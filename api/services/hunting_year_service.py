from uuid import UUID
from typing import List, Optional

from repositories.hunting_year_repository import HuntingYearRepository
from core.database.models import HuntingYear
from core.exceptions import NotFoundException, ConflictException, ValidationException
from datetime import date
import re
import logging


logger = logging.getLogger(__name__)


class HuntingYearService:
    def __init__(self, hunting_year_repository: HuntingYearRepository):
        self.hunting_year_repository = hunting_year_repository

    async def create_hunting_year(self, start_year: int, is_current: bool = False, is_locked: bool = False) -> HuntingYear:

        name = f"{start_year}/{start_year + 1}"

        if not re.match(r'^\d{4}/\d{4}$', name):
            logger.error("Invalid HuntingYear name format.")
            raise ValidationException(
                detail="Name must be in the format 'YYYY/YYYY'.")

        start_year_parsed, end_year_parsed = map(int, name.split('/'))
        if end_year_parsed != start_year_parsed + 1:
            logger.error(
                "End year is not exactly one greater than start year.")
            raise ValidationException(
                detail="The second year must be exactly one greater than the first year.")

        existing = await self.hunting_year_repository.get_by_name(name)
        if existing:
            logger.error(f"HuntingYear with name '{name}' already exists.")
            raise ConflictException(
                detail=f"HuntingYear with name '{name}' already exists.")

        if is_current:
            current_hunting_year = await self.hunting_year_repository.get_current_hunting_year()
            if current_hunting_year:
                logger.error("There is already a current HuntingYear.")
                raise ConflictException(
                    detail="There is already a current HuntingYear. Unset it before setting a new one as current.")

        start_date = date(start_year, 7, 1)
        end_date = date(start_year + 1, 6, 30)

        hunting_year = await self.hunting_year_repository.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
            is_locked=is_locked
        )

        if is_current and current_hunting_year:
            current_hunting_year.is_current = False
            await self.hunting_year_repository.update(current_hunting_year)

        logger.info(f"Created new HuntingYear: {hunting_year.name}")
        return hunting_year

    async def get_hunting_year(self, hunting_year_id: UUID) -> HuntingYear:
        hunting_year = await self.hunting_year_repository.read(hunting_year_id)
        if not hunting_year:
            logger.error(f"HuntingYear with ID {hunting_year_id} not found")
            raise NotFoundException(
                detail=f"HuntingYear with ID {hunting_year_id} not found")
        return hunting_year

    async def list_hunting_years(self, limit: int = 100, offset: int = 0) -> List[HuntingYear]:
        hunting_years = await self.hunting_year_repository.list_hunting_years_descending(limit=limit, offset=offset)
        if not hunting_years:
            logger.error(f"No HuntingYears found.")
            raise NotFoundException(detail="No HuntingYears found.")
        return hunting_years

    async def set_current_hunting_year(self, hunting_year_id: UUID) -> HuntingYear:
        hunting_year = await self.hunting_year_repository.read(hunting_year_id)
        if not hunting_year:
            logger.error(f"HuntingYear with ID {hunting_year_id} not found.")
            raise NotFoundException(
                detail=f"HuntingYear with ID {hunting_year_id} not found.")

        if hunting_year.is_current:
            logger.info(f"HuntingYear {hunting_year.name} is already current.")
            return hunting_year

        current_hunting_year = await self.hunting_year_repository.get_current_hunting_year()
        if current_hunting_year:
            current_hunting_year.is_current = False
            await self.hunting_year_repository.update(current_hunting_year)
            logger.info(
                f"Unset current HuntingYear: {current_hunting_year.name}")

        hunting_year.is_current = True
        await self.hunting_year_repository.update(hunting_year)
        logger.info(f"Set HuntingYear {hunting_year.name} as current.")
        return hunting_year

    async def lock_hunting_year(self, hunting_year_id: UUID) -> HuntingYear:
        hunting_year = await self.hunting_year_repository.read(hunting_year_id)
        if not hunting_year:
            logger.error(f"HuntingYear with ID {hunting_year_id} not found.")
            raise NotFoundException(
                detail=f"HuntingYear with ID {hunting_year_id} not found.")

        if hunting_year.is_locked:
            logger.info(f"HuntingYear {hunting_year.name} is already locked.")
            return hunting_year

        hunting_year.is_locked = True
        await self.hunting_year_repository.update(hunting_year)
        logger.info(f"Locked HuntingYear {hunting_year.name}.")
        return hunting_year

    async def unlock_hunting_year(self, hunting_year_id: UUID) -> HuntingYear:
        hunting_year = await self.hunting_year_repository.read(hunting_year_id)
        if not hunting_year:
            logger.error(f"HuntingYear with ID {hunting_year_id} not found.")
            raise NotFoundException(
                detail=f"HuntingYear with ID {hunting_year_id} not found.")

        if not hunting_year.is_locked:
            logger.info(
                f"HuntingYear {hunting_year.name} is already unlocked.")
            return hunting_year

        hunting_year.is_locked = False
        await self.hunting_year_repository.update(hunting_year)
        logger.info(f"Unlocked HuntingYear {hunting_year.name}.")
        return hunting_year

    async def resolve_hunting_year(self, hunting_year_id: Optional[UUID] = None) -> HuntingYear:
        
        logger.info(f"resolve hunting year: {hunting_year_id} <-")
        if hunting_year_id:
            hunting_year = await self.get_hunting_year(hunting_year_id)
            logger.info(hunting_year)
            return hunting_year
        else:
            hunting_year = await self.hunting_year_repository.get_current_hunting_year()
            if not hunting_year:
                logger.error("No current Hunting year is set.")
                raise NotFoundException(detail="No current HuntingYear is set.")
            return hunting_year