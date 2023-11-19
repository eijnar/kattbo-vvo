from app import db
from app.events.models import UsersEvents

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
