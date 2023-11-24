from app import db
from flask import current_app
from app.events.models import UsersEvents, Event, EventDayGathering, EventDay
from app.utils.notification import get_opted_in_users_for_event_notification, send_sms
from app.utils.models import NotificationType
from datetime import datetime


def handle_user_event_day_registration(user_id, days_ids):
    try:
        submitted_day_ids = set(days_ids)
        current_registrations = UsersEvents.query.filter_by(
            user_id=user_id).all()
        current_registered_day_ids = {
            reg.day_id for reg in current_registrations}

        day_ids_to_add = submitted_day_ids - current_registered_day_ids
        day_ids_to_remove = current_registered_day_ids - submitted_day_ids

        for day_id in day_ids_to_add:
            new_registration = UsersEvents(user_id=user_id, day_id=day_id)
            db.session.add(new_registration)

        for day_id in day_ids_to_remove:
            registrations_to_remove = UsersEvents.query.filter_by(
                user_id=user_id, day_id=day_id)
            for registration in registrations_to_remove:
                db.session.delete(registration)

        db.session.commit()
        return True

    except Exception as e:
        print(e)
        db.session.rollback()
        return False


def create_event_and_gatherings(form, current_user):
    try:
        event = Event(
            event_type_id=form.event_type.data,
            description=form.description.data,
            creator_id=current_user.id
        )
            
        db.session.add(event)
        db.session.flush()  # This will assign an ID to the event without committing the transaction

        dates = [d.strip() for d in form.dates.data.split(',')]
        for date_str in dates:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            event_day = EventDay(event_id=event.id, date=date)
            db.session.add(event_day)

        if form.joint_gathering.data:
            selected_place_id = form.joint_gathering_place.data
            create_event_day_gatherings(event, selected_place_id, None)
        else:
            hemmalaget_place_id = form.hemmalaget_gathering_place.data
            bortalaget_place_id = form.bortalaget_gathering_place.data
            hemmalaget_team_id = 1
            bortalaget_team_id = 2
            create_event_day_gatherings(event, hemmalaget_place_id, hemmalaget_team_id)
            create_event_day_gatherings(event, bortalaget_place_id, bortalaget_team_id)
        
        db.session.commit()
        return event
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return False

def create_event_day_gatherings(event, place_id, team_id):
    try:
        for event_day in event.event_days:
            gathering = EventDayGathering(
                event_day_id = event_day.id,
                place_id = place_id,
                team_id = team_id
            )
            db.session.add(gathering)
        db.session.commit()
        return True
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return False
    
def notify_users_about_event(event, form):
    notification_types = NotificationType.query.all()

    urlshortener = current_app.urlshortener

    if event:
        event_type_name = event.event_type.name
        event_days_list = sorted([event_day.date for event_day in event.event_days])
        gathering_message = get_notification_message(event)

    for notification_type in notification_types:
        users_to_notify = get_opted_in_users_for_event_notification(form.event_type.data, notification_type.id)
        for user in users_to_notify:
            if notification_type.name == 'SMS':
                event_days_str = ', '.join(day.strftime("%d/%m") for day in event_days_list)
                jwt_payload = {'user_id': user.id, 'event_id': event.id}
                shortlink = urlshortener.create_short_link_with_jwt(jwt_payload)
                message = f'Hej {user.first_name}!\nVälkommen på {event_type_name.lower()} {event_days_str}.\n\n{gathering_message}\n\nKlicka på länken för att anmäla dig samt få mer information: {shortlink}'
                # send_sms(user.phone_number, message)
                print(message)

            if notification_type.name == 'E-post':
                print("Skickar E-post")

def get_notification_message(event):
    if event.event_days:
        # Get the first day and its start time
        first_day = sorted(event.event_days, key=lambda x: x.date)[0]
        start_time = first_day.start_time.strftime('%H:%M') if first_day.start_time else "ingen specifik tid"
        end_time = first_day.end_time.strftime('%H:%M') if first_day.end_time else "ingen specifik tid"
        event_category_name = event.event_type.event_category.name.lower()

        if event_category_name.lower() == 'meeting':
            # Assuming there's always a location for the meeting
            place = first_day.gatherings[0].place.name if first_day.gatherings else "okänd plats"
            return f'Mötet hålls i {place.lower()} från kl {start_time} till ca. {end_time}'

        elif event_category_name.lower() == 'hunting':
            if any(g.team is None for g in first_day.gatherings):
                place = next(g.place.name for g in first_day.gatherings if g.team is None)
                return f'Vi samlas gemensamt vid {place.lower()} kl {start_time}'

            # Handle separate gatherings for the first day
            gatherings_info = [f'{g.team.name} samlas vid {g.place.name}' for g in first_day.gatherings if g.team]
            if gatherings_info:
                return ', '.join(gatherings_info) + f' kl {start_time}'

    return "Samlingsinformation ej tillgänglig"
