from flask_security import current_user, login_required, roles_accepted
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort, make_response, current_app
from app import db, celery
from flask_jwt_extended import decode_token
from app.events.forms import EventForm, RegisterEventDayForm
from app.events.models import Event, EventDay, UsersEvents, EventType, EventCategory
from app.users.models import User, UsersTags
from app.tag.models import Tag
from app.hunting.models import UserTeamYear, HuntTeam, StandAssignment, Stand, AnimalQuota
from app.utils.models import Document, NotificationTask
from app.map.models import PointOfIntrest
from app.events.utils import handle_user_event_day_registration, create_event_and_gatherings
from app.utils.notification import notify_users_about_event
from pdfkit import from_string
from markdown import markdown
from datetime import datetime
from collections import defaultdict
from celery.result import AsyncResult


events = Blueprint('events', __name__, template_folder='templates')

#
# This section doesn't require to be logged in
#

@events.route('/quick_registration', methods=['GET'])
def quick_register():
    token = request.args.get('token')

    if not token:
        flash('No token provided.')
        return redirect(url_for('main.home'))

    try:
        # Decode the token to get the event ID and user identity
        decoded_token = decode_token(token)
        event_id = decoded_token['sub']['event_id']
        user_id = decoded_token['sub']['user_id']
        print(f'Event id: {event_id}\nUser_id {user_id}')

        # Retrieve the event including its event days using the relationship
        event = Event.query.filter_by(id=event_id).first()
        event_type = EventType.query.filter_by(id = event.event_type_id).first()
        pm = Document.query.filter_by(short_name='pm').first()

        def get_quota_statistics(hunt_year_id):
            quotas = AnimalQuota.query.filter_by(hunt_year_id=hunt_year_id).all()
            statistics = {}

            for quota in quotas:
                team_name = quota.hunt_team.name
                animal_name = quota.animal_type.name
                remaining_quota = quota.initial_quota - len(quota.animals_shot)

                if team_name not in statistics:
                    statistics[team_name] = {}

                statistics[team_name][animal_name] = remaining_quota
                
            return statistics

        statistics = get_quota_statistics(1)
        if event is None:
            flash('Event not found.')
            return redirect(url_for('main.home'))

        # Check if the user is already registered for this event
        for event_day in event.event_days:
            if UsersEvents.query.filter_by(user_id=user_id, day_id=event_day.id).first():
                flash('You are already registered for one or more days of this event.')
                return render_template('events/registration_confirmation.html.j2', pm=markdown(pm.document), event=event, event_type=event_type, statistics=statistics)

        # If not already registered, register the user for all event days
        for event_day in event.event_days:
            user_event = UsersEvents(user_id=user_id, day_id=event_day.id)
            db.session.add(user_event)

        db.session.commit()


        # Redirect to a confirmation page or back to the homepage
        flash('You have successfully registered for the event!')
        return render_template('events/registration_confirmation.html.j2', pm=markdown(pm.document), event=event, event_type=event_type, statistics=statistics, form=form)
    
    except Exception as e:
        return e


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
    # Subquery for EventDay with future dates
    future_event_days = db.session.query(EventDay.event_id).filter(
        EventDay.date > datetime.utcnow()
    ).subquery()

    # Query Event objects
    query = Event.query.join(
        future_event_days, Event.id == future_event_days.c.event_id
    ).join(
        EventDay, EventDay.event_id == Event.id
    ).join(
        EventType, EventType.id == Event.event_type_id
    ).join(
        EventCategory, EventCategory.id == EventType.event_category_id
    )
    # Filter by event category if provided
    if event_category is not None:
        query = query.filter(EventCategory.name == event_category)

    # Fetch events, grouped by Event
    events = query.group_by(Event.id).order_by(
        db.func.min(EventDay.date)  # Order by the earliest EventDay date
    ).all()

    return render_template('events/list_events.html.j2', events=events, teams=teams)


@events.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def create_event():
    event_category_name = request.args.get('event_category')
    event_category = EventCategory.query.filter_by(name=event_category_name).first()
    event_types = EventType.query.filter_by(event_category_id=event_category.id).all()
    event_form = EventForm()
    gathering_places = PointOfIntrest.query.filter_by(category='gathering_place')
    default_hemmalaget_name = "Sågen"
    default_bortalaget_name = "Slaktladan"
    default_joint_gathering_place_name = "Slaktladan"

    # Populate choices for gathering places
    event_form.event_type.choices = [(et.id, et.name) for et in event_types]
    event_form.joint_gathering_place.choices = [(jg.id, jg.name) for jg in gathering_places]
    event_form.hemmalaget_gathering_place.choices = [(hg.id, hg.name) for hg in gathering_places]
    event_form.bortalaget_gathering_place.choices = [(bg.id, bg.name) for bg in gathering_places]

    default_hemmalaget_id = next((place.id for place in gathering_places if place.name == default_hemmalaget_name), None)
    default_bortalaget_id = next((place.id for place in gathering_places if place.name == default_bortalaget_name), None)
    default_joint_gathering_place_id = next((place.id for place in gathering_places if place.name == default_joint_gathering_place_name), None)

    if default_hemmalaget_id is not None:
        event_form.hemmalaget_gathering_place.data = default_hemmalaget_id
    if default_bortalaget_id is not None:
        event_form.bortalaget_gathering_place.data = default_bortalaget_id
    if default_joint_gathering_place_id is not None:
        event_form.joint_gathering_place.data = default_joint_gathering_place_id


    if event_form.validate_on_submit():
        new_event = create_event_and_gatherings(event_form, current_user)
        task = notify_users_about_event.apply_async(args=[new_event.id, event_form.event_type.data], countdown=20)
        notification_task = NotificationTask(
            celery_task_id=task.id,
            event_id=new_event.id,
            event_type=event_form.event_type.data
        )
        db.session.add(notification_task)
        db.session.commit()

        flash('The event has been created!', 'success')
        if event_category_name is not None:
            return redirect(url_for('events.list_events') + '?event_category=' + event_category_name)
        else:
            return redirect(url_for('events.list_events'))
        
    else:
        print("Form errors:", event_form.errors)
    return render_template('events/create_event.html.j2', event_form=event_form, event_category=event_category)


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

    return render_template('events/accept_event.html.j2', form=form, event=event, user_subscriptions=user_subscriptions)


@events.route('/<int:event_id>/_pdf', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def generate_event_pdf(event_id):
    current_app.logger.info(f'{current_user.email} is creating a PDF')
    event_days = EventDay.query.filter_by(event_id=event_id).all()

    users_by_team_and_day = {}
    specific_tags = ['doghandler', 'shooter', 'hunt-leader']
    team_id = request.args.get('team_id')

    if team_id is not None:
        teams = [team_id]
    else:
        teams = [HuntTeam.id for huntteam in HuntTeam.query.all()]

    organized_data = []
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

        users_by_team_and_day = {}
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
    
    rendered_page = render_template(
        'events/pdf/attendance.html.j2', data=organized_data)

    pdf = from_string(rendered_page, False, options=get_pdf_options())

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=VVO-Deltagarlista.pdf'

    return response


@events.route('/<int:event_id>/cancel', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'hunt-leader')
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator_id != current_user.id:
        abort(403)

    # Check if all event days are already cancelled
    if all(event_day.cancelled for event_day in event.event_days):
        flash('Evenemanget har redan blivit inställt.', 'info')
        return redirect(url_for('events.list_events'))  # Redirect to a relevant page

    try:
        
        for event_day in event.event_days:
            event_day.cancelled = True
        db.session.commit()

        if not abort_task(event_id):
            notify_users_about_event.delay(event.id, event.event_type.id, cancelled=True)

        flash(f'Du har ställt in {event.event_type.name}', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Ett fel inträffade när evenemanget skulle avbrytas: {str(e)}', 'error')

    return redirect(url_for('events.list_events'))  # Redirect to a relevant page after processing

def abort_task(event_id):
    task = NotificationTask.query.filter_by(event_id=event_id).first()
    if task:
        celery.control.revoke(task.celery_task_id)
        task_result = AsyncResult(task.celery_task_id)
        current_app.logger.info(task_result)
        return True
    return False