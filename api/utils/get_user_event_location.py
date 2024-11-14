
from logging import getLogger


logger = getLogger(__name__)

async def get_user_event_location(event_data, user_team_id):
    """
    Get the location for the user's event considering team-specific gathering places.
    
    Args:
        event_data (EventDay): The EventDay SQLAlchemy model instance.
        user_team_id (UUID): The ID of the user's team.

    Returns:
        dict: A dictionary with the location name, latitude, and longitude, or None if no location is found.
    """
    try:
        logger.debug(f"Fetching locations for EventDay ID: {event_data.id}")
        
        # Access gathering places from the relationship
        locations = event_data.event_day_gathering_places
        logger.debug(f"Found {len(locations)} gathering place(s) for the event.")

        selected_location = None

        # If there is only one location without a team_id, it's a joint gathering place
        if len(locations) == 1 and locations[0].team_id is None:
            selected_location = locations[0]
            logger.debug("Joint gathering place found.")
        else:
            # Find the location specific to the user's team
            selected_location = next(
                (loc for loc in locations if loc.team_id == user_team_id),
                None
            )
            if selected_location:
                logger.debug(f"Team-specific gathering place found for team {user_team_id}.")
            else:
                logger.warning(f"No specific gathering place found for team {user_team_id}. Falling back to the first location.")
                selected_location = locations[0] if locations else None

        if selected_location and selected_location.gathering_place:
            waypoint = selected_location.gathering_place
            latitude = waypoint.latitude
            longitude = waypoint.longitude

            if latitude is not None and longitude is not None:
                logger.debug(f"Waypoint '{waypoint.name}' coordinates: ({latitude}, {longitude})")
                return {
                    "location_name": waypoint.name,
                    "latitude": latitude,
                    "longitude": longitude,
                }
            else:
                logger.error(f"Waypoint '{waypoint.name}' has invalid or missing coordinates.")
                return None
        else:
            logger.error("No valid gathering place or waypoint found.")
            return None

    except Exception as e:
        logger.exception(f"Error occurred while fetching user event location: {e}")
        return None