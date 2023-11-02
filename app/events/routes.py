from flask_security import current_user, login_required
from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from datetime import datetime
from app.events.models import Event, EventDay, UserEvent
from app.events.forms import EventForm, RegisterEventDayForm
from app.tags.models import Tags

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/event')
def list_events():
    events = Event.query.all()
    return render_template('events/list_events.html.j2', events=events)

@events.route('/create', methods=['GET', 'POST'])
def create_event():
    event_form = EventForm()
    event_form.tags.choices = [(t.id, t.name) for t in Tags.query.all()]  # Populate choices for tags field
    
    if event_form.validate_on_submit():
        event = Event(
            name=event_form.name.data,
            event_type=event_form.event_type.data,  # Handle event_type
            description=event_form.description.data,
            creator_id=current_user.id
        )
        db.session.add(event)
        db.session.flush()  # This will assign an ID to the event without committing the transaction

        # Handle tags
        for tag_id in event_form.tags.data:
            tag = Tags.query.get(tag_id)
            if tag:
                event.tags.append(tag)

        dates = [d.strip() for d in event_form.dates.data.split(',')]
        for date_str in dates:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            event_day = EventDay(event_id=event.id, date=date)
            db.session.add(event_day)

        db.session.commit()
        flash('The event has been created!', 'success')
        return redirect(url_for('events.create_event'))
    else:
        print("Form errors:", event_form.errors)  # Add this line
    return render_template('events/create_event.html.j2', event_form=event_form)

@events.route('/register_event_day/<int:event_id>', methods=['GET', 'POST'])
@login_required
def register_event_day(event_id):
    event = Event.query.get_or_404(event_id)
    form = RegisterEventDayForm()
    form.event_days.choices = [(ed.id, ed.date) for ed in event.days]

    if form.validate_on_submit():
        day_ids = form.event_days.data
        user_id = current_user.id

        for day_id in day_ids:
            # Check if user is already registered for the event day
            existing_registration = UserEvent.query.filter_by(user_id=user_id, day_id=day_id).first()
            if not existing_registration:
                registration = UserEvent(user_id=user_id, day_id=day_id)
                db.session.add(registration)

        db.session.commit()
        flash('You have successfully registered for the event days!', 'success')
        return redirect(url_for('events.register_event_day', event_id=event_id))

    # Select all event days by default
    form.event_days.data = [choice[0] for choice in form.event_days.choices]

    return render_template('events/register_event_day.html', form=form, event=event)