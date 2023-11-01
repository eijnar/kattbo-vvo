from app import app, db
from flask_security import auth_required, roles_accepted, current_user, permissions_accepted
from flask import redirect, url_for, flash, request, render_template, jsonify
from app.user.forms import UpdateProfileForm, OptInFormMeta
from app.models import Subject, UserSubject

@app.route('/profile/update', methods=['GET', 'POST'])
@auth_required()
def update_profile():
    user = current_user
    profile_form = UpdateProfileForm()
    subjects = Subject.query.all()
    OptInForm = OptInFormMeta(subjects)
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
        for subject in subjects:
            email_field = 'subject_email_' + str(subject.id)
            sms_field = 'subject_sms_' + str(subject.id)
            user_subject = UserSubject.query.filter_by(
                user_id=current_user.id,
                subject_id=subject.id,
            ).first()
            if user_subject is None:
                user_subject = UserSubject(
                    user_id=current_user.id,
                    subject_id=subject.id,
                )
                db.session.add(user_subject)
            user_subject.opt_in_email = getattr(opt_in_form, email_field).data
            user_subject.opt_in_sms = getattr(opt_in_form, sms_field).data
        db.session.commit()
        flash('Du har uppdaterat dina kontaktvägar!', 'success')
        return redirect(url_for('update_profile'))
    

    elif request.method == 'GET':
        profile_form.email.data = current_user.email
        profile_form.phone_number.data = current_user.phone_number
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        for subject in subjects:
            user_subject = UserSubject.query.filter_by(user_id=user.id, subject_id=subject.id).first()
            if user_subject:
                email_field = getattr(opt_in_form, 'subject_email_' + str(subject.id))
                sms_field = getattr(opt_in_form, 'subject_sms_' + str(subject.id))
                email_field.data = user_subject.opt_in_email
                sms_field.data = user_subject.opt_in_sms
    return render_template('user/update_profile.html', title='Update Profile', profile_form=profile_form, subjects=subjects, opt_in_form=opt_in_form, user=current_user)