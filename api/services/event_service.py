from typing import List, Optional
from logging import getLogger
from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from core.exceptions import NotFoundError, ValidationError, DatabaseError
from core.database.models import Event, EventDay, EventDayGatheringPlace
from schemas.event.event import EventResponse, EventCreate
from repositories import (
    EventRepository,
    EventDayRepository,
    EventDayGatheringRepository,
    EventCategoryRepository,
    UserRepository,
    TeamRepository,
    WaypointRepository
)


logger = getLogger(__name__)


class EventService:
    def __init__(
        self,
        event_repository=EventRepository,
        event_day_repository=EventDayRepository,
        event_day_gathering_repository=EventDayGatheringRepository,
        event_category_repository=EventCategoryRepository,
        user_repository=UserRepository,
        team_repository=TeamRepository,
        waypoint_repository=WaypointRepository
    ):
        self.event_repository = event_repository
        self.event_day_repository = event_day_repository
        self.event_day_gathering_repository = event_day_gathering_repository
        self.event_category_repository = event_category_repository
        self.user_repository = user_repository
        self.team_repository = team_repository
        self.waypoint_repository = waypoint_repository


    async def get_all_event_days(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EventResponse]:

        events = await self.event_day_repository.list_by_date_range(limit=limit, offset=offset, start=start, end=end)
        if not events:
            raise NotFoundError(detail="No events found")
        return events
    
    async def get_all_events_with_days(
        self,
        start: Optional[date] = None,
        end: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[EventResponse]:

        events = await self.event_repository.list_events_with_days_by_date_range(limit=limit, offset=offset, start=start, end=end)
        if not events:
            raise NotFoundError(detail="No events found")
        return events

    async def get_event(self, id: str) -> EventResponse:
        event = await self.event_repository.read(id)
        days = await self.event_day_repository.filter(event_id=event.id, order_by="date")
        return event, days

    async def create_event(self, event_create: EventCreate) -> Event:
        logger.debug("Trying to create event")
        try:

            # Validate creator
            logger.debug("Validating creator")
            creator = await self.user_repository.read(event_create.creator_id)
            if not creator:
                logger.error(f"Creator not found: {event_create.creator_id}")
                raise NotFoundError(
                    detail=f"Creator not found: {event_create.creator_id}"
                )

            # Validate Event Category
            logger.debug("Validating event category")
            event_category = await self.event_category_repository.read(event_create.event_category_id)
            if not event_category:
                logger.error(
                    f"Event category not found: {event_create.event_category_id}")
                raise NotFoundError(
                    detail=f"Event category not found: {event_create.event_category_id}"
                )

            # Validating gathering places
            gathering_place_ids = {
                gp.gathering_place_id
                for day in event_create.days
                for gp in day.event_day_gathering_places
            }
            logger.debug(f"Validating gathering places: {gathering_place_ids}")
            if gathering_place_ids:
                existing_gathering_places = await self.waypoint_repository.get_all_by_ids(list(gathering_place_ids))
                if len(existing_gathering_places) != len(gathering_place_ids):
                    missing = gathering_place_ids - \
                        {gp.id for gp in existing_gathering_places}
                    logger.error(f"Gathering places not found: {missing}")
                    raise ValidationError(
                        detail=f"Gathering places not found: {missing}"
                    )

            # Validate Teams
            logger.debug("Validating teams")
            team_ids = {
                gp.team_id
                for day in event_create.days
                for gp in day.event_day_gathering_places
                if gp.team_id
            }

            if team_ids:
                existing_teams = await self.team_repository.get_all_by_ids(list(team_ids))
                if len(existing_teams) != len(team_ids):
                    missing = team_ids - {team.id for team in existing_teams}
                    logger.error(f"Teams not found: {missing}")
                    raise ValidationError(
                        detail=f"Teams not found: {missing}")

            # Create Event Instance
            logger.debug("Creating Event instance")
            event = Event(
                name=event_create.name,
                event_category_id=event_create.event_category_id,
                creator_id=event_create.creator_id,
            )
            logger.debug("Step 3 complete")

            # Create EventDay and EventDayGatheringPlace Instances
            for day_create in event_create.days:
                try:
                    logger.debug(
                        f"Creating EventDay with start date: {day_create.start_datetime} and end date: {day_create.end_datetime}")
                    event_day = EventDay(
                        start_datetime=day_create.start_datetime,
                        end_datetime=day_create.end_datetime
                    )
                    # Establish relationship
                    event.event_days.append(event_day)

                    for gp_assignment in day_create.event_day_gathering_places:
                        logger.debug(
                            f"Creating EventDayGatheringPlace for gathering_place_id {gp_assignment.gathering_place_id}")
                        gathering = EventDayGatheringPlace(
                            gathering_place_id=gp_assignment.gathering_place_id,
                            team_id=gp_assignment.team_id
                        )
                        event_day.event_day_gathering_places.append(
                            gathering)  # Establish relationship
                except Exception as inner_e:
                    logger.error(
                        f"Error creating EventDay or GatheringPlace: {inner_e}", exc_info=True)
                    raise

            # Persist to Database within a Transaction
            logger.debug("Persisting Event to database")
            await self.event_repository.create_event(event_data=event)
            logger.debug("Event persisted successfully")

            # aReturn the ORM Event Object Directly
            return event

        except ValidationError as ve:
            logger.error(f"Validation error: {ve.detail}")
            raise ve
        except NotFoundError as ne:
            logger.error(f"Not found error: {ne.detail}")
            raise ne
        except SQLAlchemyError as sae:
            logger.error(f"Database error: {sae}")
            raise DatabaseError(
                detail="An error occurred while creating the event.") from sae
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise DatabaseError(
                detail="An unexpected error occurred.") from e
