import gpxpy.gpx
import gpxpy
from app import db
from flask import Blueprint, redirect, current_app, render_template, current_app, g, jsonify
from app.utils.notification import send_sms
from app.utils.forms import NotificationForm, SearchForm
from models.utils import NotificationTask
from celery.result import AsyncResult
from app import celery
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from models.hunting import Stand
from models.maps import PointOfIntrest
from sqlalchemy import and_

utils = Blueprint('utils', '__name__', template_folder='templates')

@utils.route('/health')
def health():
    try:
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "reason": str(e)}), 500

@utils.route('/<short_code>')
def redirect_to_original_url(short_code):
    urlshortener = current_app.urlshortener
    original_url = urlshortener.get_original_url(short_code)
    print(original_url)
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

@utils.before_request
def before_request():
    g.search_form = SearchForm()

@utils.route('/import_gpx')
def import_gpx():
    with open('test.gpx', 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for waypoint in gpx.waypoints:
        point = Point(waypoint.longitude, waypoint.latitude)
        geopoint = from_shape(point)

        if ':' in waypoint.name and '&' not in waypoint.name:
            area_id, number = waypoint.name.split(':')
            if int(area_id) == 0 or Stand.query.filter_by(area_id=int(area_id), number=number).first():
                unmatched_point = PointOfIntrest(name=waypoint.name, category='auto', geopoint=geopoint)
                db.session.add(unmatched_point)
            else:
                stand = Stand(number=number, geopoint=geopoint, area_id=int(area_id))
                db.session.add(stand)

        elif '&' in waypoint.name and all(':' in part for part in waypoint.name.split(' & ')):
            entries = waypoint.name.split(' & ')
            for entry in entries:
                area_id, number = entry.split(':')
                if int(area_id) == 0 or Stand.query.filter_by(area_id=int(area_id), number=number).first():
                    unmatched_point = PointOfIntrest(name=entry, category='auto', geopoint=geopoint)
                    db.session.add(unmatched_point)
                else:
                    stand = Stand(number=number, geopoint=geopoint, area_id=int(area_id))
                    db.session.add(stand)

        else:
            unmatched_point = PointOfIntrest(name=waypoint.name, category='auto', geopoint=geopoint)
            db.session.add(unmatched_point)

    db.session.commit()


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
