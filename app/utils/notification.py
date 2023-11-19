from app import db
from app.utils.models import NotificationType, TagsNotifications
from app.tag.models import Tag
from app.events.models import EventType, EventTypeTags
from app.users.models import RolesTags, Role, RolesUsers, User, UserNotificationPreference
from phonenumbers import format_number, PhoneNumberFormat, parse
from requests import post

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

def send_sms(number, message):
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
    response = post(url, headers=headers, data=data)
    return response.status_code, response.text