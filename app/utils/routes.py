import logging
from flask import Blueprint, redirect, current_app, render_template, jsonify, current_app
from flask_security import login_required, roles_accepted
from app.utils.notification import send_sms
from app.utils.forms import NotificationForm
from app.utils.models import NotificationTask
from celery.result import AsyncResult
from app import celery

utils = Blueprint('utils', '__name__', template_folder='templates')

@utils.route('/<short_code>')
def redirect_to_original_url(short_code):
    urlshortener = current_app.urlshortener
    original_url = urlshortener.get_original_url(short_code)
    print(original_url)
    if original_url is not None:
        return redirect(original_url)
    else:
        print("hejsan")
        return 'URL not found', 404
    
@utils.route('/notification', methods=['GET', 'POST'])
def send_notification():
    form = NotificationForm()

    if form.validate_on_submit():
        send_sms('0702598032', form.message.data)

    return render_template('send_message.html.j2', form=form)

class TaskStateException(Exception):
    pass

def cancel_event_notifications(event_id):
    """
    Cancel event notifications for a given event_id.

    Args:
        event_id (int): The ID of the event.

    Returns:
        dict: A dictionary with a status and message indicating the result of the cancellation.
    """
    if not isinstance(event_id, int):
        raise TypeError("Invalid event_id parameter. Expected an integer.")

    task = NotificationTask.query.filter_by(
        event_id=event_id, 
    ).one_or_none()

    if task:
        if validate_task_id(task.celery_task_id):
            current_app.logger.info(task)
            celery.control.revoke(task.celery_task_id, terminate=True, signal='SIGTERM')
            task_result = AsyncResult(task.celery_task_id)  # Recheck state
            raise TaskStateException(f"Task {task.celery_task_id} state: {task_result.state}")
        else:
            raise ValueError('Invalid task ID')

    return {'status': 'success', 'message': 'Event notifications cancelled.'}
