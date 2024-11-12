from uuid import UUID
from typing import List
from logging import getLogger

from sqlalchemy import desc, asc
from sqlalchemy.exc import SQLAlchemyError

from core.exceptions import NotFoundException, ConflictException, ValidationException, DatabaseException
from core.database.models import Event, EventDay, EventDayGatheringPlace
from repositories import EventRepository, EventDayRepository, EventDayGatheringRepository, TeamRepository
from schemas.event.event import EventBase, EventResponse, EventList, EventCreate


logger = getLogger(__name__)


class EventService:
    def __init__(
        self,
        event_repository=EventRepository,
        event_day_repository=EventDayRepository,
        event_day_gathering_repository=EventDayGatheringRepository,
        team_repository=TeamRepository
    ):
        self.event_repository = event_repository
        self.event_day_repository = event_day_repository
        self.event_day_gathering_repository = event_day_gathering_repository
        self.team_repository = team_repository

    async def get_all_events(self, limit: int = 100, offset: int = 0) -> List[EventBase]:
        events = await self.event_repository.list(limit=limit, offset=offset)
        if not events:
            raise NotFoundException(detail="No events found")
        return events

    async def get_event(self, id: str) -> EventResponse:
        event = await self.event_repository.read(id)
        days = await self.event_day_repository.filter(event_id=event.id, order_by="date")
        return event, days
    
    async def create_event(self, event_create: EventCreate) -> Event:
        logger.debug("Trying to create event")
        try:
            # Step 1: Validate Teams
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
                    raise ValidationException(detail=f"Teams not found: {missing}")

            # Step 2: Create Event Instance
            logger.debug("Creating Event instance")
            event = Event(
                name=event_create.name,
                event_category_id=event_create.event_category_id,
                creator_id=event_create.creator_id,
            )
            logger.debug("Step 3 complete")

            # Step 3: Create EventDay and EventDayGatheringPlace Instances
            for day_create in event_create.days:
                try:
                    logger.debug(f"Creating EventDay for date {day_create.date}")
                    event_day = EventDay(
                        date=day_create.date,
                        start_time=day_create.start_time,
                        end_time=day_create.end_time
                    )
                    event.event_days.append(event_day)  # Establish relationship

                    for gp_assignment in day_create.event_day_gathering_places:
                        logger.debug(f"Creating EventDayGatheringPlace for gathering_place_id {gp_assignment.gathering_place_id}")
                        gathering = EventDayGatheringPlace(
                            gathering_place_id=gp_assignment.gathering_place_id,
                            team_id=gp_assignment.team_id
                        )
                        event_day.event_day_gathering_places.append(gathering)  # Establish relationship
                except Exception as inner_e:
                    logger.error(f"Error creating EventDay or GatheringPlace: {inner_e}", exc_info=True)
                    raise

            # Step 4: Persist to Database within a Transaction
            logger.debug("Persisting Event to database")
            await self.event_repository.create_event(event_data=event)
            logger.debug("Event persisted successfully")

            # Step 5: Return the ORM Event Object Directly
            return event

        except ValidationException as ve:
            logger.error(f"Validation error: {ve.detail}")
            raise ve
        except NotFoundException as ne:
            logger.error(f"Not found error: {ne.detail}")
            raise ne
        except SQLAlchemyError as sae:
            logger.error(f"Database error: {sae}")
            raise DatabaseException(detail="An error occurred while creating the event.") from sae
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise DatabaseException(detail="An unexpected error occurred.") from e