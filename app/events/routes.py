from flask_security import current_user, login_required
from flask import Blueprint, current_app, render_template, flash, redirect, url_for, request
from sqlalchemy.orm import aliased
from app import db
from flask_jwt_extended import decode_token
from datetime import datetime
from app.events.models import Event, EventDay, UsersEvents
from app.events.forms import EventForm, RegisterEventDayForm
from app.users.models import User
from app.tag.models import Tag, TagCategory, TagsCategories

events = Blueprint('events', __name__, template_folder='templates')


@events.route('/')
def list_events():

    events = db.session.query(
        Event,
        db.func.count(
            db.func.distinct(UsersEvents.user_id)).label('subscriber_count')
    ).join(
        EventDay, EventDay.event_id == Event.id
    ).outerjoin(
        UsersEvents, UsersEvents.day_id == EventDay.id
    ).group_by(
        Event
    ).having(
        db.func.max(EventDay.date) > datetime.utcnow()
    ).order_by(
        db.func.min(EventDay.date)
    ).all()

    return render_template('events/list_events.html.j2', events=events)


@events.route('/create', methods=['GET', 'POST'])
def create_event():
    urlshortener = current_app.urlshortener
    event_form = EventForm()

    # Populate choices for tags field
    event_form.tag_category.choices = [
        (tc.id, tc.name) for tc in TagCategory.query
        .join(TagsCategories)
        .join(Tag)
        .filter(Tag.name == 'event_enabled')
        .all()
    ]

    if event_form.validate_on_submit():
        event = Event(
            tag_category_id=event_form.tag_category.data,
            description=event_form.description.data,
            creator_id=current_user.id
        )
        db.session.add(event)
        db.session.flush()  # This will assign an ID to the event without committing the transaction
        dates = [d.strip() for d in event_form.dates.data.split(',')]
        for date_str in dates:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = time.strptime(event_form.time.data, '%HH%MM').date()
            event_day = EventDay(event_id=event.id, date=date, time=time)
            db.session.add(event_day)

        db.session.commit()

        users = User.query.all()
        for user in users:
            jwt_payload = {'user_id': user.id, 'event_id': event.id}
            urlshortener.create_short_link_with_jwt(jwt_payload)

        flash('The event has been created!', 'success')
        return redirect(url_for('events.create_event'))
    else:
        print("Form errors:", event_form.errors)  # Add this line
    return render_template('events/create_event.html.j2', event_form=event_form)


@events.route('/quick_registration', methods=['GET'])
def quick_register():
    token = request.args.get('token')
    decoded_token = decode_token(token)
    print(decoded_token)
    if not token:
        flash('No token provided.')
        return redirect(url_for('main.home'))

    try:
        # Decode the token to get the event ID and user identity
        decoded_token = decode_token(token)
        event_id = decoded_token['sub']['event_id']
        user_id = decoded_token['sub']['user_id']

        # Retrieve the event including its event days using the relationship
        event = Event.query.filter_by(id=event_id).first()
        if event is None:
            flash('Event not found.')
            return redirect(url_for('main.home'))

        # Check if the user is already registered for this event
        for event_day in event.days:
            if UserEvent.query.filter_by(user_id=user_id, day_id=event_day.id).first():
                flash('You are already registered for one or more days of this event.')
                return redirect(url_for('main.home'))

        # If not already registered, register the user for all event days
        for event_day in event.days:
            user_event = UserEvent(user_id=user_id, day_id=event_day.id)
            db.session.add(user_event)

        db.session.commit()
        flash('You have successfully registered for the event!')

    except Exception as e:
        # Handle exceptions, such as token expiration or decoding errors
        flash(str(e))

    # Redirect to a confirmation page or back to the homepage
    return redirect(url_for('main.home'))

@events.route('/register/sms', methods=['GET', 'POST'])
def register_with_sms():
    data = request.data
    print(data)
    return jsonify(data)

@events.route('/<int:event_id>/register', methods=['GET', 'POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = RegisterEventDayForm()
    form.event_days.choices = [(ed.id, ed.date) for ed in event.event_days]

    if form.validate_on_submit():
        day_ids = form.event_days.data
        user_id = current_user.id

        for day_id in day_ids:
            # Check if user is already registered for the event day
            existing_registration = UsersEvents.query.filter_by(
                user_id=user_id, day_id=day_id).first()
            if not existing_registration:
                registration = UsersEvents(user_id=user_id, day_id=day_id)
                db.session.add(registration)

        db.session.commit()
        flash('You have successfully registered for the event days!', 'success')
        return redirect(url_for('events.list_events', event_id=event_id))

    # Select all event days by default
    form.event_days.data = [choice[0] for choice in form.event_days.choices]

    return render_template('events/event_form.html.j2', form=form, event=event)
