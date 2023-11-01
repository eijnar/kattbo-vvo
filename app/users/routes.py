from app import db
from flask_security import auth_required, roles_accepted, current_user, permissions_accepted
from flask import Blueprint redirect, url_for, flash, request, render_template, jsonify
from app.users.forms import UpdateProfileForm, OptInFormMeta
from app.users.models import UserTags
from app.tags.models import Tags

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/profile/update', methods=['GET', 'POST'])
@auth_required()
def update_profile():
    user = current_user
    profile_form = UpdateProfileForm()
    tags = Tags.query.all()
    OptInForm = OptInFormMeta(tags)
    opt_in_form = OptInForm()
    if profile_form.validate_on_submit() and profile_form.submit.data:
        current_user.email = profile_form.email.data
        current_user.phone_number = profile_form.phone_number.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        db.session.commit()
        flash('Din profil har blivit uppdaterad', category='success')
        return redirect(url_for('update_profile'))
    elif opt_in_form.validate_on_submit() and opt_in_form.submit.data:
        for tag in tags:
            email_field = 'tag_email_' + str(tag.id)
            sms_field = 'tag_sms_' + str(tag.id)
            user_tag = UserTag.query.filter_by(
                user_id=current_user.id,
                tag_id=tag.id,
            ).first()
            if user_tag is None:
                user_tag = UserTag(
                    user_id=current_user.id,
                    tag_id=tag.id,
                )
                db.session.add(user_tag)
            user_tag.opt_in_email = getattr(opt_in_form, email_field).data
            user_tag.opt_in_sms = getattr(opt_in_form, sms_field).data
        db.session.commit()
        flash('Du har uppdaterat dina kontaktvägar!', 'success')
        return redirect(url_for('update_profile'))
    

    elif request.method == 'GET':
        profile_form.email.data = current_user.email
        profile_form.phone_number.data = current_user.phone_number
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        for tag in tags:
            user_tag = UserTags.query.filter_by(user_id=user.id, tag_id=tag.id).first()
            if user_tag:
                email_field = getattr(opt_in_form, 'tag_email_' + str(tag.id))
                sms_field = getattr(opt_in_form, 'tag_sms_' + str(tag.id))
                email_field.data = user_tag.opt_in_email
                sms_field.data = user_tag.opt_in_sms
    return render_template('users/update_profile.html', title='Update Profile', profile_form=profile_form, tags=tags, opt_in_form=opt_in_form, user=current_user)