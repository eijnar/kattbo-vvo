from app import db
from flask_security import login_required, current_user
from flask import Blueprint, redirect, url_for, flash, request, render_template
from app.utils.notification import get_notification_options_for_user, get_distinct_notification_types_for_user
from app.blueprints.users.forms import UpdateProfileForm, UserPreferenceFormFactory
from app.models.users import User, UserNotificationPreference
from app.models.tag import Tag


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/user/preferences', methods=['GET', 'POST'])
@login_required
def edit_preferences():
    user = User.query.filter(user.id == current_user.id).first()
    form = UserNotificationPreference(user=user)

    if form.validate_on_submit():
        for field in form:
            if field.name.startswith('opt_in_'):
                tag_id = int(field.name.split('_')[3])
                tag = Tag.query.get(tag_id)
                user.set_opt_in(tag, field.data)
        db.session.commit()
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('edit_preferences'))

    return render_template('users/edit_preferences.html', form=form)


@users.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = current_user
    notification_options = get_notification_options_for_user(user)
    user_notification_types = get_distinct_notification_types_for_user(user)


    # Get the users opt_ins to display in form
    user_prefs_query = UserNotificationPreference.query.filter_by(
        user_id=user.id)
    user_preferences = {
        (pref.event_type_id, pref.notification_type_id): pref.opt_in
        for pref in user_prefs_query
    }

    # Use the factory to dynamically get TagCategories user can subscribe to
    UserPreferenceForm = UserPreferenceFormFactory(
        notification_options, user_preferences)

    # Define the forms
    profile_form = UpdateProfileForm()
    opt_in_form = UserPreferenceForm()

    if profile_form.validate_on_submit() and profile_form.submit.data:
        current_user.email = profile_form.email.data
        current_user.phone_number = profile_form.phone_number.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
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
                    user_id=user.id,
                    event_type_id=event_type.id,
                    notification_type_id=notification_type.id
                ).first()

                if preference:
                    preference.opt_in = opt_in_value
                else:
                    new_preference = UserNotificationPreference(
                        event_type_id=event_type.id,
                        user_id=user.id,
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
    from app.models.users import Role, RolesTags, RolesUsers
    from app.models.events import EventType, EventTypeTags
    from app.models.utils import TagsNotifications, NotificationType
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