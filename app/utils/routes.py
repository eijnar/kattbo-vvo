from flask import Blueprint, redirect, current_app, render_template
from flask_security import login_required, roles_accepted
from app.utils.notification import send_sms
from app.utils.forms import NotificationForm

utils = Blueprint('utils', '__name__', template_folder='templates')

@utils.route('/<short_code>')
def redirect_to_original_url(short_code):
    urlshortener = current_app.urlshortener
    original_url = urlshortener.get_original_url(short_code)

    if original_url is not None:
        return redirect(original_url)
    else:
        return 'URL not found', 404
    
@utils.route('/notification', methods=['GET', 'POST'])
def send_notification():
    form = NotificationForm()

    if form.validate_on_submit():
        send_sms('0702598032', form.message.data)

    return render_template('send_message.html.j2', form=form)