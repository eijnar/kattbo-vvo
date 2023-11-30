from app import db
from flask import current_app, render_template
from app.events.models import UsersEvents, Event, EventDayGathering, EventDay
from app.utils.notification import get_opted_in_users_for_event_notification, send_sms
from app.utils.models import NotificationType
from datetime import datetime


class NotificationSender:
    def __init__(self, user, event):
        self.user = user
        self.event = event

    def send(self):
        raise NotImplementedError
    
class SMSNotificationSender(NotificationSender):
    def send(self, message_builder):
        message = message_builder.build_message()
        send_sms(self.user.phone_number, message)

class EmailNotificationSender(NotificationSender):
    def send(self):
        pass

class NotificationFactory:
    @staticmethod
    def get_notification_sender(notification_type, user, event):
        if notification_type == 'SMS':
            return SMSNotificationSender(user, event)
        elif notification_type == 'E-post':
            return EmailNotificationSender(user, event)
        else:
            raise ValueError("Unsupported notification type")

class MessageBuilder:
    def __init__(self, event, user, urlshortener, notification_type, cancelled=False):
        self.user = user
        self.event = event
        self.urlshortener = urlshortener
        self.cancelled = cancelled
        self.notification_type = notification_type
        self.event_type = event.event_type.name.lower()

    def build_message(self):
        context = self.get_template_context()
        template_prefix = 'cancel' if self.cancelled else 'event'
        template_name = f'messages/{template_prefix}_{self.event_type}_{self.notification_type}.html'

        return render_template(template_name, **context)

    def get_template_context(self):
        event_type_name = self.event.event_type.name
        event_days_list = sorted([event_day.date for event_day in self.event.event_days])

        if len(event_days_list) > 1:
            event_days_str = f"{event_days_list[0].strftime('%d/%m -%y')} till {event_days_list[-1].strftime('%d/%m -%y')}"
        else:
            event_days_str = event_days_list[0].strftime('%d/%m')

        gathering_message = self.get_gathering_message()
        jwt_payload = {'user_id': self.user.id, 'event_id': self.event.id}
        shortlink = self.urlshortener.create_short_link_with_jwt(jwt_payload)

        return {
            'user_first_name': self.user.first_name,
            'event_type_name': event_type_name.lower(),
            'event_days_str': event_days_str,
            'gathering_message': gathering_message,
            'shortlink': shortlink
        }

    def get_gathering_message(self):
        if not self.event.event_days:
            return "Samlingsinformation ej tillgänglig"

        first_day = sorted(self.event.event_days, key=lambda x: x.date)[0]
        start_time = first_day.start_time.strftime('%H:%M') if first_day.start_time else "ingen specifik tid"
        end_time = first_day.end_time.strftime('%H:%M') if first_day.end_time else "ingen specifik tid"
        event_category_name = self.event.event_type.event_category.name.lower()

        if event_category_name == 'meeting':
            place = first_day.gatherings[0].place.name if first_day.gatherings else "okänd plats"
            return f'Mötet hålls i {place.lower()} från kl {start_time} till ca. {end_time}'

        elif event_category_name == 'hunting':
            gatherings_info = []
            for gathering in first_day.gatherings:
                team_name = gathering.team.name if gathering.team else "Vi"
                place_name = gathering.place.name
                gatherings_info.append(f'{team_name} samlas vid {place_name}')

            if gatherings_info:
                return ', '.join(gatherings_info) + f' kl {start_time}'
            else:
                return 'Inga samlingsplatser tillgängliga för första dagen'

        return "Samlingsinformation ej tillgänglig"


def notify_users_about_event(event, notification_type_param, cancelled=False):
    notification_types = NotificationType.query.all()
    urlshortener = current_app.urlshortener  # Assuming urlshortener is set up in your app context

    for notification_type in notification_types:
        users_to_notify = get_opted_in_users_for_event_notification(notification_type_param, notification_type.id)

        for user in users_to_notify:
            sender = NotificationFactory.get_notification_sender(notification_type.name, user, event)
            message_builder = MessageBuilder(event, user, urlshortener, notification_type.name.lower(), cancelled=cancelled)
            sender.send(message_builder)


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
