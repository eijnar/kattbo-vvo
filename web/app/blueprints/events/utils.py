from app import db
from models.events import UsersEvents, Event, EventDayGathering, EventDay
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
            creator_id=current_user.id,
        )
            
        db.session.add(event)
        db.session.flush()  # This will assign an ID to the event without committing the transaction

        dates = [d.strip() for d in form.dates.data.split(',')]
        for date_str in dates:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            event_day = EventDay(event_id=event.id, date=date, start_time=form.start_time.data)
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
