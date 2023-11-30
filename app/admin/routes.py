from app import db
from flask_security import login_required, roles_accepted, login_required
from flask import Blueprint, render_template, request, jsonify, session
from app.users.models import User, UsersTags
from app.tag.models import Tag, TagsCategories, TagCategory
from app.hunting.models import UserTeamYear, HuntYear, HuntTeam, StandAssignment, Stand
from collections import defaultdict
from app.admin.forms import EditUserForm

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route("/user/<int:user_id>")
@login_required
@roles_accepted('admin', 'hunt-leader')
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    tags = Tag.query.join(TagsCategories, Tag.id == TagsCategories.tag_id) \
                    .join(TagCategory, TagCategory.id == TagsCategories.tag_category_id) \
                    .filter(TagCategory.name == 'hunter') \
                    .all()
    stand_query = db.session.query(Stand.number) \
        .join(StandAssignment, Stand.id == StandAssignment.stand_id) \
        .filter(StandAssignment.user_id == user_id) \
        .filter(StandAssignment.hunt_year_id == 1) \
        .group_by(Stand.number) \
        .all()
    for stand_tuple in stand_query:
        stand = stand_tuple[0]


    return render_template('admin/edit_user.html.j2', user=user, tags=tags, stand=stand)


@admin.route("/edit/<int:selected_hunt_year_id>")
@login_required
@roles_accepted('admin', 'hunt-leader')
def edit_hunt_teams(selected_hunt_year_id):
    form = EditUserForm()
    users = User.query.all()
    teams = HuntTeam.query.all()
    year = HuntYear.query.filter_by(id=selected_hunt_year_id).first()
    print(f'År: {selected_hunt_year_id}')
    # Query for the specific TagCategory
    tag_category_name = 'hunter'

    tag_category = TagCategory.query.filter_by(name=tag_category_name).first()

    tags = Tag.query.join(TagsCategories).filter(
        TagsCategories.tag_category_id == tag_category.id).all()

    hunters = User.query \
        .outerjoin(UserTeamYear, (UserTeamYear.user_id == User.id) & (UserTeamYear.hunt_year_id == selected_hunt_year_id)) \
        .outerjoin(UsersTags) \
        .outerjoin(Tag, Tag.id == UsersTags.tag_id) \
        .outerjoin(TagsCategories, Tag.id == TagsCategories.tag_id) \
        .outerjoin(TagCategory, TagCategory.id == TagsCategories.tag_category_id) \
        .all()

    team_users = defaultdict(list)
    unassigned_key = 'Ej tilldelade'

    for user in hunters:
        # Check if the user is assigned to a team for the selected hunt year
        user_team_year = next((uty for uty in user.hunt_years if uty.hunt_year_id == selected_hunt_year_id), None)

        if user_team_year and user_team_year.hunt_team:
            team_name = user_team_year.hunt_team.name
        else:
            team_name = unassigned_key

        team_users[team_name].append(user)


    return render_template('admin/manage_huntteam.html.j2', users=users, teams=teams, year=year, team_users=team_users, tags=tags, form=form)


@admin.route("/add_hunt_team", methods=["POST"])
@login_required
@roles_accepted('admin', 'hunt-leader')
def add_hunt_team():
    form = EditUserForm()
    user_id = request.form.get('user_id')
    hunt_team_id = request.form.get('hunt_team_id')
    hunt_year_id = request.form.get('hunt_year_id')

    def assign_user_to_stands(user_id, stand_number):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        stands = Stand.query.filter_by(number=stand_number).all()

        for stand in stands:
            assignment = StandAssignment(user_id=user.id, stand_id=stand.id, hunt_year_id=hunt_year_id)
            db.session.add(assignment)

        db.session.commit()

    def reassign_user_to_new_team(user_id, hunt_team_id, hunt_year_id):
        # Find the existing assignment
        existing_assignment = UserTeamYear.query.filter_by(
            user_id=user_id,
            hunt_year_id=hunt_year_id
        ).first()

        if existing_assignment:
            # Update the existing assignment with the new team
            existing_assignment.hunt_team_id = hunt_team_id
        else:
            # If there was no existing assignment, create a new one
            new_assignment = UserTeamYear(
                user_id=user_id,
                hunt_team_id=hunt_team_id,
                hunt_year_id=hunt_year_id
            )
            db.session.add(new_assignment)

        db.session.commit()

    if form.validate_on_submit():
        reassign_user_to_new_team(user_id, hunt_team_id, hunt_year_id)
        # assign_user_to_stands(user_id, stand_number)
        return jsonify({'status': 'success', 'message': 'User added to team successfully'})
    else:
        print(form.errors)
        return jsonify({'status': 'error', 'message': 'Invalid form data you punk'})

