from app import db
from flask_security import auth_required, current_user
from flask import Blueprint, redirect, url_for, flash, request, render_template
from app.utils.notification import get_notification_options_for_user, get_distinct_notification_types_for_user
from app.users.forms import UpdateProfileForm, UserPreferenceFormFactory
from app.users.models import User, UserNotificationPreference
from app.tag.models import Tag


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/user/preferences', methods=['GET', 'POST'])
@auth_required
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
@auth_required()
def update_profile():
    user = current_user
    notification_options = get_notification_options_for_user(user)
    user_notification_types = get_distinct_notification_types_for_user(user)

    # Get the users opt_ins to display in form
    user_prefs_query = UserNotificationPreference.query.filter_by(
        user_id=user.id)
    user_preferences = {
        (pref.tag_category_id, pref.notification_type_id): pref.opt_in
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
        for tag_category, notification_types in notification_options.items():
            for notification_type in notification_types:
                field_name = f'notification_{tag_category.id}_{notification_type.id}'
                opt_in_value = getattr(opt_in_form, field_name).data
                # Query the existing preference
                preference = UserNotificationPreference.query.filter_by(
                    user_id=user.id,
                    tag_category_id=tag_category.id,
                    notification_type_id=notification_type.id
                ).first()

                if preference:
                    preference.opt_in = opt_in_value
                else:
                    new_preference = UserNotificationPreference(
                        tag_category_id=tag_category.id,
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
