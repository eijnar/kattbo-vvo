import os
from app import db
from flask_security import login_required, current_user
from flask import Blueprint, redirect, url_for, flash, request, render_template, send_from_directory, current_app
from app.utils.notification import get_notification_options_for_user, get_distinct_notification_types_for_user
from app.blueprints.users.forms import UpdateProfileForm, UserPreferenceFormFactory
from models.users import User, UserNotificationPreference
from models.tag import Tag
from .utils import FileUploadHandler



users = Blueprint('users', __name__, template_folder='templates')

@users.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    notification_options = get_notification_options_for_user(current_user)
    user_notification_types = get_distinct_notification_types_for_user(current_user)

    # Get the users opt_ins to display in form
    user_prefs_query = UserNotificationPreference.query.filter_by(
        user_id=current_user.id)
    user_preferences = {
        (pref.event_type_id, pref.notification_type_id): pref.opt_in
        for pref in user_prefs_query
    }

    # Use the factory to dynamically get TagCategories user can subscribe to
    UserPreferenceForm = UserPreferenceFormFactory(
        notification_options, user_preferences)

    upload_handler = FileUploadHandler(
        allowed_extensions=['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.md'],
        base_upload_folder=current_app.config['UPLOAD_FOLDER'],
        size=(200, 200)
    )
    # Define the forms
    profile_form = UpdateProfileForm()
    opt_in_form = UserPreferenceForm()

    if profile_form.validate_on_submit() and profile_form.submit.data:
        current_user.email = profile_form.email.data
        current_user.phone_number = profile_form.phone_number.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.profile_picture = upload_handler.save_file(profile_form.profile_picture.data, is_public=True)
        db.session.commit()
        flash('Din profil har blivit uppdaterad', category='success')
        return redirect(url_for('users.update_profile'))
    
    elif opt_in_form.validate_on_submit():
        for event_type, notification_types in notification_options.items():
            for notification_type in notification_types:
                field_name = f'notification_{event_type.id}_{notification_type.id}'
                opt_in_value = getattr(opt_in_form, field_name).data
                # Query the existing preference
                preference = UserNotificationPreference.query.filter_by(
                    user_id=current_user.id,
                    event_type_id=event_type.id,
                    notification_type_id=notification_type.id
                ).first()

                if preference:
                    preference.opt_in = opt_in_value
                else:
                    new_preference = UserNotificationPreference(
                        event_type_id=event_type.id,
                        user_id=current_user.id,
                        notification_type_id=notification_type.id,
                        opt_in=opt_in_value
                    )
                    print(f'New preference: {new_preference} \n')
                    db.session.add(new_preference)
        db.session.commit()

        flash('Your preferences have been updated.')
        return redirect(url_for('users.update_profile'))

    elif request.method == 'GET':
        profile_form.email.data = current_user.email
        profile_form.phone_number.data = current_user.phone_number
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name

    return render_template(
        'users/update_profile.html.j2',
        title='Update Profile',
        profile_form=profile_form,
        notification_options=notification_options,
        user_notification_types=user_notification_types,
        opt_in_form=opt_in_form,
        user=current_user
    )


@users.route('test')
def test_user():
    from models.users import Role, RolesTags, RolesUsers
    from models.events import EventType, EventTypeTags
    from models.utils import TagsNotifications, NotificationType
    user = User.query.filter(User.id == current_user.id).first()
    if user:
        print("User found:", user)
    else:
        print("User not found")

    roles = Role.query.join(RolesUsers, Role.id == RolesUsers.role_id).filter(RolesUsers.user_id == user.id).all()
    if roles:
        print("Roles associated with user:", roles)
    else:
        print("No roles associated with this user")


    tags = Tag.query.join(RolesTags, Tag.id == RolesTags.tag_id).join(Role, RolesTags.role_id == Role.id).filter(Role.id.in_([role.id for role in roles])).all()
    if tags:
        print("Tags associated with roles:", tags)
    else:
        print("No tags associated with these roles")

    event_types = EventType.query.join(EventTypeTags, EventType.id == EventTypeTags.event_id).join(Tag, EventTypeTags.tag_id == Tag.id).filter(Tag.id.in_([tag.id for tag in tags])).all()
    notification_types = NotificationType.query.join(TagsNotifications, NotificationType.id == TagsNotifications.notification_type_id).join(Tag, TagsNotifications.tag_id == Tag.id).filter(Tag.id.in_([tag.id for tag in tags])).all()

    if event_types:
        print("Event types associated with tags:", event_types)
    else:
        print("No event types associated with these tags")

    if notification_types:
        print("Notification types associated with tags:", notification_types)
    else:
        print("No notification types associated with these tags")

    print("----------------------------------")

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
    
    test = get_opted_in_users_for_event_notification(1, 2)
    print(test)
    return "<html></html>"

@users.route("/profile_picture/<path:filename>")
def profile_picture(filename):
    public_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'public', filename)
    return send_from_directory(public_directory)