from typing import Optional
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from models.hunting import HuntYear
from datetime import date


class CurrentHuntYearNotSetError(Exception):
    pass

class NoPreviousHuntYearFoundError(Exception):
    pass

class HuntYearFinder:
    def __init__(self):
        self.today = None

    def _find_current_hunt_year(self):
        if self.today is None:
            self.today = date.today()
        try:
            current_hunt_year = HuntYear.query.filter(
                HuntYear.start_date <= self.today,
                HuntYear.end_date >= self.today
            ).first()
        except SQLAlchemyError as e:
            current_app.logger.error("An error occurred during database operations: %s", str(e))
            current_hunt_year = None
        return current_hunt_year

    @property
    def current(self) -> Optional[HuntYear]:
        """
        Get the current hunt year.

        Returns:
            Optional[HuntYear]: The current hunt year, or None if not set.
        """
        current_hunt_year = self._find_current_hunt_year()
        return current_hunt_year

    def find_hunt_year(self, direction):
        if self.current is None:
            raise CurrentHuntYearNotSetError("Current hunt year is not set.")
        if direction == 'previous':
            return HuntYear.query.filter(
                HuntYear.end_date < self.current.start_date
            ).order_by(HuntYear.end_date.desc()).first()
        elif direction == 'next':
            return HuntYear.query.filter(
                HuntYear.start_date > self.current.end_date
            ).order_by(HuntYear.start_date).first()
        else:
            raise ValueError("Invalid direction parameter.")

    def previous(self):
        previous_hunt_year = self.find_hunt_year('previous')
        if previous_hunt_year is None:
            raise NoPreviousHuntYearFoundError("No previous hunt year found.")
        return previous_hunt_year

    def next(self):
        return self.find_hunt_year('next')