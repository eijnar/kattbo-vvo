from app import db
from app.utils.models import NotificationType, TagsNotifications
from app.tag.models import Tag, TagCategory, TagsCategories
from app.users.models import RolesTags, Role, RolesUsers, User

def get_notification_options_for_user(user):
    # Get a list of tuples where each tuple contains a TagCategory and the associated NotificationTypes
    notification_options = (
        db.session.query(TagCategory, NotificationType)
        .join(TagsCategories, TagCategory.id == TagsCategories.tag_category_id)
        .join(Tag, TagsCategories.tag_id == Tag.id)
        .join(RolesTags, Tag.id == RolesTags.tag_id)
        .join(Role, RolesTags.role_id == Role.id)
        .join(RolesUsers, Role.id == RolesUsers.role_id)
        .join(User, RolesUsers.user_id == User.id)
        .join(TagsNotifications, Tag.id == TagsNotifications.tag_id)
        .join(NotificationType, TagsNotifications.notification_type_id == NotificationType.id)
        .filter(User.id == user.id)
        .distinct()
        .order_by(TagCategory.id, NotificationType.id)
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