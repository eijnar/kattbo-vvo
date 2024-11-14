from logging import getLogger
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from icalendar import (
    Calendar, 
    Event as ICalEvent, 
    vCalAddress, 
    vText, 
    vGeo, 
    vRecur, 
    Timezone, 
    TimezoneStandard, 
    TimezoneDaylight
)

from utils.get_user_event_location import get_user_event_location

logger = getLogger(__name__)

def build_vtimezone(timezone: str):
    """Helper to build a VTIMEZONE component."""

    tz = Timezone()
    tz.add('TZID', timezone)
    tz.add('X-LIC-LOCATION', timezone)

    # Standard time
    standard = TimezoneStandard()
    standard.add('DTSTART', datetime(1970, 10, 25, 2, 0, 0))
    standard.add('TZOFFSETFROM', timedelta(hours=2))
    standard.add('TZOFFSETTO', timedelta(hours=1))
    standard.add('RRULE', vRecur({"FREQ": "YEARLY", "BYMONTH": 10, "BYDAY": "-1SU"}))
    tz.add_component(standard)

    # Daylight saving time
    daylight = TimezoneDaylight()
    daylight.add('DTSTART', datetime(1970, 3, 29, 2, 0, 0))
    daylight.add('TZOFFSETFROM', timedelta(hours=1))
    daylight.add('TZOFFSETTO', timedelta(hours=2))
    daylight.add('RRULE', vRecur({"FREQ": "YEARLY", "BYMONTH": 3, "BYDAY": "-1SU"}))
    tz.add_component(daylight)

    return tz

async def generate_ical(events):
    
    cal = Calendar()
    cal.add('X-WR-CALNAME', 'Kättbo VVO')
    cal.add('PRODID', vText('KattboVVO/web/SE'))
    cal.add('VERSION', vText('2.0'))
    
    timezone = 'Europe/Stockholm'
    cal.add_component(build_vtimezone(timezone))
    
    for event_day in events:
        event = ICalEvent()
        event['uid'] = str(event_day.id)
        event.add('summary', event_day.event.name)
        
        start_time = event_day.start_datetime.astimezone(ZoneInfo(timezone))
        end_time = event_day.end_datetime.astimezone(ZoneInfo(timezone))
        
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        event.add('dtstamp', event_day.created_at)
        event.add('sequence', event_day.sequence)
        event.add('status', 'CANCELLED' if event_day.cancelled else 'CONFIRMED')

        creator = event_day.event.creator
        creator_email_str = creator.email
        creator_name_str = f"{creator.first_name} {creator.last_name}"
        creator_phone_number_str = creator.phone_number
        
        organizer = vCalAddress(f'MAILTO:{creator_email_str}')
        organizer.params['cn'] = vText(creator_name_str)
        event['organizer'] = organizer
        event.add('contact', vText(f'{creator_name_str}, {creator_phone_number_str}'))
        
        event.add('categories', event_day.event.event_category.name.upper())

        location_info = await get_user_event_location(event_day, None)
        logger.debug(f"location_info: {location_info}")
        if location_info:
            event.add('location', vText(location_info["location_name"]))
            event.add('geo', vGeo((location_info["latitude"], location_info["longitude"])))
            event.add('X-APPLE-STRUCTURED-LOCATION', f'geo:{location_info["latitude"]},{location_info["longitude"]}', parameters={
                'VALUE': 'URI',
                'X-APPLE-MAPKIT-HANDLE': '',
                'X-APPLE-RADIUS': '80',
                'X-TITLE': location_info['location_name']
            })
        
        for attendee_registration in event_day.user_events:  # Assuming user_events is a list of UserEventRegistration
            user = attendee_registration.user  # Assuming UserEventRegistration has a 'user' relationship
            attendee_email = user.email
            attendee_name = f"{user.first_name} {user.last_name}"

            attendee_ical = vCalAddress(f'MAILTO:{attendee_email}')
            attendee_ical.params['cn'] = vText(attendee_name)
            attendee_ical.params['CUTYPE'] = vText('INDIVIDUAL')
            attendee_ical.params['ROLE'] = vText('REQ-PARTICIPANT')
            attendee_ical.params['PARTSTAT'] = vText("ACCEPTED")
            attendee_ical.params['RSVP'] = vText("TRUE")

            event.add('attendee', attendee_ical, encode=0)

        cal.add_component(event)
        
    return cal.to_ical()