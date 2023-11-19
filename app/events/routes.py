from flask_security import current_user, login_required, roles_accepted
from flask import Blueprint, current_app, render_template, flash, redirect, url_for, request, abort, make_response
from app import db
from flask_jwt_extended import decode_token
from datetime import datetime
from app.events.forms import EventForm, RegisterEventDayForm
from app.events.models import Event, EventDay, UsersEvents, EventType, EventCategory
from app.users.models import User, UsersTags
from app.tag.models import Tag
from app.hunting.models import UserTeamYear, HuntTeam, StandAssignment, Stand
from app.utils.models import Document, NotificationType
from app.utils.notification import get_opted_in_users_for_event_notification, send_sms
from app.events.utils import handle_user_event_day_registration
from pdfkit import from_string
from markdown import markdown
from collections import defaultdict


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
        for event_day in event.event_days:
            if UsersEvents.query.filter_by(user_id=user_id, day_id=event_day.id).first():
                flash('You are already registered for one or more days of this event.')
                return render_template(url_for('events.registration_confirmation'))

        # If not already registered, register the user for all event days
        for event_day in event.event_days:
            user_event = UsersEvents(user_id=user_id, day_id=event_day.id)
            db.session.add(user_event)

        db.session.commit()
        flash('You have successfully registered for the event!')
        return render_template(url_for('events.registration_confirmation'))

    except Exception as e:
        # Handle exceptions, such as token expiration or decoding errors
        flash(str(e))

    pm = Document.query.filter_by(short_name='pm').first()
    event_type = EventType.query.filter_by(id = event.event_type_id).first()
    # Redirect to a confirmation page or back to the homepage
    return render_template('events/registration_confirmation.html.j2', pm=markdown(pm.document), event=event, event_type=event_type)


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

    return render_template('events/list_events.html.j2', events=events, teams=teams)


@events.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def create_event():
    event_category_name = request.args.get('event_category')
    event_category = EventCategory.query.filter_by(name=event_category_name).first()
    event_types = EventType.query.filter_by(event_category_id=event_category.id).all()
    urlshortener = current_app.urlshortener
    event_form = EventForm()

    # Populate choices for tags field
    event_form.event_type.choices = [(et.id, et.name) for et in event_types]

    if event_form.validate_on_submit():

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
        
        notification_types = NotificationType.query.all()
        event = Event.query.filter_by(id=event.id).first()
        
        if event:
            event_type_name = event.event_type.name
            event_days_list = sorted([event_day.date for event_day in event.event_days])

        for notification_type in notification_types:
            users_to_notify = get_opted_in_users_for_event_notification(event_form.event_type.data, notification_type.id)
            for user in users_to_notify:
                if notification_type.name == 'SMS':
                    event_days_str = ', '.join(day.strftime("%d/%m") for day in event_days_list)
                    jwt_payload = {'user_id': user.id, 'event_id': event_form.event_type.data}
                    shortlink = urlshortener.create_short_link_with_jwt(jwt_payload)
                    message = f'Hej {user.first_name}!\n Välkommen på {event_type_name.lower()} {event_days_str}.\n\nKlicka på länken för att anmäla dig samt få mer information: {shortlink}'
                    send_sms(user.phone_number, message)
                if notification_type.name == 'E-post':
                    print("Skickar E-post")

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
        user_id = current_user.id
        day_ids = form.event_days.data
        success = handle_user_event_day_registration(user_id, day_ids)
        if success:
            flash('Din registreting har hanterats', 'success')
        else:
            flash('Det blev något fel när vi hanterade din registrering', 'error')
        return redirect(url_for('events.list_events', event_id=event_id))

    # Select all event days by default
    form.event_days.data = [choice[0] for choice in form.event_days.choices]

    event_days = EventDay.query.filter_by(event_id=event_id).all()

    # Organize users and their subscribed days
    user_subscriptions = defaultdict(list)
    for day in event_days:
        for users_event in day.users_events:
            user_subscriptions[users_event.user].append(day.date)

    return render_template('events/event_form.html.j2', form=form, event=event, user_subscriptions=user_subscriptions)


@events.route('/<int:event_id>/_pdf', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def generate_event_pdf(event_id):
    event_days = EventDay.query.filter_by(event_id=event_id).all()

    users_by_team_and_day = {}
    specific_tags = ['doghandler', 'shooter', 'hunt-leader']
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
            .outerjoin(StandAssignment, StandAssignment.user_id == User.id) \
            .outerjoin(Stand, Stand.id == StandAssignment.stand_id) \
            .add_columns(HuntTeam.name, HuntTeam.id, EventDay.date, Tag.name, Stand.number) \
            .distinct() \
            .all()

    for user, team_name, team_id, event_date, tag_name, stand_number in users_in_day:
        team_key = (team_id, team_name)
        if team_key not in users_by_team_and_day:
            users_by_team_and_day[team_key] = {}
        if event_date not in users_by_team_and_day[team_key]:
            users_by_team_and_day[team_key][event_date] = {'users': []}

        user_info = {
            'user': user,
            'tag': tag_name,
            'stand': stand_number if stand_number else None
        }
        users_by_team_and_day[team_key][event_date]['users'].append(user_info)

    organized_data = []

    for (team_id, team_name), dates in users_by_team_and_day.items():
        for date, data in dates.items():
            users_by_specific_tags = {tag: [] for tag in specific_tags}

            for user_info in data['users']:
                user_data = {
                    'user_details': user_info['user'],
                    'stand_number': user_info['stand']
                }
                if user_info['tag'] in specific_tags:
                    users_by_specific_tags[user_info['tag']].append(user_data)

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
    
    print(organized_data)
    rendered_page = render_template(
        'events/pdf/attendance.html.j2', data=organized_data)

    pdf = from_string(rendered_page, False, options=get_pdf_options())

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=VVO-Deltagarlista.pdf'

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
