import re
import logging
import requests
from app import db, create_app
from flask import render_template, current_app
from app.models.utils import NotificationType, TagsNotifications
from app.models.tag import Tag
from app.models.events import EventType, EventTypeTags
from app.models.users import RolesTags, Role, RolesUsers, User, UserNotificationPreference
from phonenumbers import format_number, PhoneNumberFormat, parse
from flask_mailman import EmailMessage
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from app.models.events import Event


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
    def send(self, message_builder):
        message = message_builder.build_message()
        event_type = message_builder.event.event_type.name
        subject = f'Välkommen på {event_type.lower()}!'
        send_email_task(self.user.email, subject, message)

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


@shared_task(base=AbortableTask)
def notify_users_about_event(event_id, notification_type_param, cancelled=False):
    with create_app().app_context():
        from flask import current_app
        event = Event.query.get(event_id)
        notification_types = (notification_type for notification_type in NotificationType.query.all())
        urlshortener = current_app.urlshortener  # Assuming urlshortener is set up in your app context

        for notification_type in notification_types:
            users_to_notify = get_opted_in_users_for_event_notification(notification_type_param, notification_type.id)

            if not users_to_notify:
                continue

            message_builder = MessageBuilder(event, None, urlshortener, notification_type.name.lower(), cancelled=cancelled)
            for user in users_to_notify:
                message_builder.user = user
                sender = NotificationFactory.get_notification_sender(notification_type.name, user, event)
                try:
                    sender.send(message_builder)
                except Exception as e:
                    # Handle the exception, log the error, or take appropriate action
                    current_app.logger.error(f"Error sending notification to user {user.id}: {str(e)}")

                # Add logging to track task progress and aid in debugging
                current_app.logger.info(f"{notification_type.name} sent to user: {user.email}")

def get_notification_options_for_user(user):
    # Get a list of tuples where each tuple contains a EventType and the associated NotificationTypes
    notification_options = (
        db.session.query(EventType, NotificationType)
        .join(EventTypeTags, EventType.id == EventTypeTags.event_id)
        .join(Tag, EventTypeTags.tag_id == Tag.id)
        .join(RolesTags, Tag.id == RolesTags.tag_id)
        .join(Role, RolesTags.role_id == Role.id)
        .join(RolesUsers, Role.id == RolesUsers.role_id)
        .join(User, RolesUsers.user_id == User.id)
        .join(TagsNotifications, Tag.id == TagsNotifications.tag_id)
        .join(NotificationType, TagsNotifications.notification_type_id == NotificationType.id)
        .filter(User.id == user.id)
        .distinct()
        .order_by(EventType.id, NotificationType.id)
        .all()
    )
    
    # Process the results to create a structure like {TagCategory: [NotificationTypes]}
    tag_category_notifications_map = {}
    for tag_category, notification_type in notification_options:
        if tag_category not in tag_category_notifications_map:
            tag_category_notifications_map[tag_category] = []
        tag_category_notifications_map[tag_category].append(notification_type)
    
    return tag_category_notifications_map

def get_distinct_notification_types_for_user(user):
    # Get a list of all the distinct notification types that a user can choose between
    user_notification_types = (
        db.session.query(NotificationType)
        .join(TagsNotifications, NotificationType.id == TagsNotifications.notification_type_id)
        .join(Tag, TagsNotifications.tag_id == Tag.id)
        .join(RolesTags, Tag.id == RolesTags.tag_id)
        .join(Role, RolesTags.role_id == Role.id)
        .join(RolesUsers, Role.id == RolesUsers.role_id)
        .join(User, RolesUsers.user_id == User.id)
        .filter(User.id == user.id)
        .distinct(NotificationType.id)
        .order_by(NotificationType.id)
        .all()
    )

    return user_notification_types

def get_opted_in_users_for_event_notification(event_type_id, notification_type_id):
    opted_in_users = (
        db.session.query(User)
        .join(UserNotificationPreference, User.id == UserNotificationPreference.user_id)
        .join(EventType, UserNotificationPreference.event_type_id == EventType.id)
        .join(NotificationType, UserNotificationPreference.notification_type_id == NotificationType.id)
        .filter(
            UserNotificationPreference.opt_in == True,
            EventType.id == event_type_id,
            NotificationType.id == notification_type_id
        )
        .distinct()
        .all()
    )
    
    return opted_in_users

def send_sms(number: str, message: str) -> tuple[int, str]:
    """
    Sends an SMS message to a specified phone number using a third-party API.

    Args:
        number (str): The phone number to send the SMS to.
        message (str): The content of the SMS message.

    Returns:
        tuple[int, str]: The HTTP status code of the API response and the text content of the API response.
    """
    country_code = 'SE'
    url = "http://172.30.150.158:8080/send"
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    parsed_number = parse(number, country_code)
    formatted_number = format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)
    formatted_number_no_spaces = formatted_number.replace(" ", "")
    data = {
        'message': message,
        'phoneno': formatted_number_no_spaces
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.text

class InvalidParameterError(Exception):
    pass

def send_email_task(email, subject, message):
    """
    Sends an email with the given email, subject, and message.
    
    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email.
    
    Returns:
        bool: True if the email sending process is successful, False otherwise.
    """
    try:
        if not isinstance(email, str):
            raise InvalidParameterError("Invalid email parameter")
        if not isinstance(subject, str):
            raise InvalidParameterError("Invalid subject parameter")
        if not isinstance(message, str):
            raise InvalidParameterError("Invalid message parameter")
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise InvalidParameterError("Invalid email format")
        
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[email]
        )
        email.send()
        return True

    except Exception as e:
        current_app.logger.exception("An error occurred while sending the email")
        return False
