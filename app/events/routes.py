from flask_security import current_user, login_required, roles_accepted
from flask import Blueprint, current_app, render_template, flash, redirect, url_for, request, abort, make_response
from app import db
from flask_jwt_extended import decode_token
from datetime import datetime
from app.events.models import Event, EventDay, UsersEvents, EventType, EventCategory
from app.events.forms import EventForm, RegisterEventDayForm
from app.users.models import User, UsersTags
from app.tag.models import Tag, TagCategory
from app.hunting.models import UserTeamYear, HuntTeam
from pdfkit import from_string

events = Blueprint('events', __name__, template_folder='templates')

#
# This section doesn't require to be logged in
#


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


#
# Login required
#


@events.route('/')
@roles_accepted('admin', 'hunt-leader', 'hunter')
@login_required
def list_events():
    event_category = request.args.get('event_category', None)

    teams = HuntTeam.query.all()

    query = db.session.query(
        Event,
        db.func.count(db.func.distinct(UsersEvents.user_id)).label('subscriber_count')
    ).join(
        Event.event_days
    ).outerjoin(
        UsersEvents, UsersEvents.day_id == EventDay.id 
    ).join(
        EventType, EventType.id == Event.event_type_id
    ).join(
        EventCategory, EventCategory.id == EventType.event_category_id
    )

    if event_category is not None:
        query = query.filter(EventCategory.name == event_category)

    events = query.group_by(
        Event
    ).having(
        db.func.max(EventDay.date) > datetime.utcnow()
    ).order_by(
        db.func.min(EventDay.date)
    ).all()
    print(events)
    return render_template('events/list_events.html.j2', events=events, teams=teams)


@events.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def create_event():
    event_category_name = request.args.get('event_category')
    event_category = EventCategory.query.filter_by(
        name=event_category_name).first()
    event_types = EventType.query.filter_by(
        event_category_id=event_category.id).all()
    urlshortener = current_app.urlshortener
    event_form = EventForm()

    # Populate choices for tags field
    event_form.event_type.choices = [
        (et.id, et.name) for et in event_types
    ]

    if event_form.validate_on_submit():
        print(event_form.event_type.data, event_form.description.data, )
        event = Event(
            event_type_id=event_form.event_type.data,
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

        users = User.query.all()
        for user in users:
            jwt_payload = {'user_id': user.id, 'event_id': event.id}
            urlshortener.create_short_link_with_jwt(jwt_payload)

        flash('The event has been created!', 'success')
        if event_category_name is not None:
            return redirect(url_for('events.list_events') + '?event_category=' + event_category_name)
        else:
            return redirect(url_for('events.list_events'))
        
    else:
        print("Form errors:", event_form.errors)  # Add this line
    return render_template('events/create_event.html.j2', event_form=event_form)


@events.route('/<int:event_id>/register', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunter', 'hunt-leader')
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


@events.route('/<int:event_id>/_pdf', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def generate_event_pdf(event_id):
    event_days = EventDay.query.filter_by(event_id=event_id).all()

    users_by_team_and_day = {}
    specific_tags = ['dogkeeper', 'shooter', 'hunt-leader']
    team_id = request.args.get('team_id')

    if team_id is not None:
        teams = [team_id]
    else:
        teams = [HuntTeam.id for huntteam in HuntTeam.query.all()]

    for event_day in event_days:
        # Fetch users and their team information for the event day
        users_in_day = User.query \
            .join(UsersEvents, UsersEvents.user_id == User.id) \
            .join(EventDay, EventDay.id == UsersEvents.day_id) \
            .filter(UsersEvents.day_id == event_day.id) \
            .join(UserTeamYear, UserTeamYear.user_id == User.id) \
            .join(HuntTeam, HuntTeam.id == UserTeamYear.hunt_team_id) \
            .join(UsersTags) \
            .join(Tag) \
            .filter(Tag.name.in_(specific_tags)) \
            .filter(HuntTeam.id.in_(teams)) \
            .add_columns(HuntTeam.name, HuntTeam.id, EventDay.date, Tag.name) \
            .distinct() \
            .all()

    for user, team_name, team_id, event_date, tag_name in users_in_day:
        team_key = (team_id, team_name)
        if team_key not in users_by_team_and_day:
            users_by_team_and_day[team_key] = {}
        if event_date not in users_by_team_and_day[team_key]:
            users_by_team_and_day[team_key][event_date] = {'users': []}

        user_info = {
            'user': user,
            'tag': tag_name
        }
        users_by_team_and_day[team_key][event_date]['users'].append(user_info)

    organized_data = []

    for (team_id, team_name), dates in users_by_team_and_day.items():
        for date, data in dates.items():
            users_by_specific_tags = {tag: [] for tag in specific_tags}

            for user_info in data['users']:
                # Check if the user's tag is in the specific tags and then add it to the corresponding list
                if user_info['tag'] in specific_tags:
                    users_by_specific_tags[user_info['tag']].append(
                        user_info['user'])

            team_info = {
                'team_id': team_id,
                'team_name': team_name,
                'date': date,
                'users_by_specific_tags': users_by_specific_tags
            }
            organized_data.append(team_info)

    def get_pdf_options():
        return {
            'page-size': 'A4',
            'encoding': 'utf-8',
            'margin-top': '12mm',
            'margin-bottom': '12mm',
            'margin-left': '12mm',
            'margin-right': '12mm'
        }
    rendered_page = render_template(
        'events/pdf/attendance.html.j2', data=organized_data)

    pdf = from_string(rendered_page, False, options=get_pdf_options())

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=your_document.pdf'

    return response


# Needs rework, new func. per EventDay has been added to the DB, cancelled defaults to False (0)
@events.route('/<int:event_id>/cancel', methods=['POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash(f'Du har tagit bort {event.tag_category.name}')
    return redirect(url_for('events.list_events'))
