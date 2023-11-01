from app import db
from datetime import datetime
from flask_security import current_user, login_required
from flask import Blueprint, render_template, flash, redirect, url_for
from app.events.models import Event, EventDay, UserEvent
from app.events.forms import EventForm, AcceptEventForm

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/event')
def list_events():
    events = Event.query.all()
    return render_template('event/list_events.html.j2', events=events)

@events.route('/event/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        db.session.commit()
        flash('The event has been updated!', 'success')
        return redirect(url_for('events.list_events'))
    return render_template('event/edit_event.html.j2', form=form, event=event)

@events.route('/event/delete/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('The event has been successfully deleted.', 'success')
    return redirect(url_for('events.create_event'))

@events.route('/event/create', methods=['GET', 'POST'])
def create_event():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(
            name=event_form.name.data,
            description=event_form.description.data,
            creator_id=current_user.id
        )
        db.session.add(event)
        db.session.flush()  # This will assign an ID to the event without committing the transaction
        
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
    return render_template('event/create_event.html.j2', event_form=event_form)

@events.route('/event/accept/<int:event_id>', methods=['GET', 'POST'])
@login_required
def accept_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = AcceptEventForm()
    form.days.choices = [(day.id, day.date) for day in event.days]
    if form.validate_on_submit():
        for day_id in form.days.data:
            user_event = UserEvent(user_id=current_user.id, day_id=day_id)
            db.session.add(user_event)
        db.session.commit()
        flash('You have successfully registered for the event!', 'success')
        return redirect(url_for('events.event_details', event_id=event.id))
    return render_template('event/list_events.html.j2', form=form, event=event)