from app import db
from flask_security import auth_required, roles_accepted, login_required
from flask import Blueprint, render_template, request, jsonify
from app.users.models import User, UsersTags
from app.tag.models import Tag, TagsCategories, TagCategory
from app.hunting.models import UserTeamYear, HuntYear, HuntTeam
from collections import defaultdict
from app.admin.forms import EditUserForm

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route("/edit_hunt_teams")
@login_required
def edit_hunt_teams():
    form = EditUserForm()
    users = User.query.all()
    teams = HuntTeam.query.all()
    years = HuntYear.query.all()

    # Query for the specific TagCategory
    category_name = 'hunter'

    tag_category = TagCategory.query.filter_by(name=category_name).first()

    tags = Tag.query.join(TagsCategories).filter(
        TagsCategories.tag_category_id == tag_category.id).all()

    # Query to get the 'main' category ID
    main_category_id = TagCategory.query.filter_by(
        name=category_name).with_entities(TagCategory.id).subquery()

    # Query users, sorting by hunting_team and including related tags
    hunters = User.query \
        .outerjoin(User.hunt_years) \
        .outerjoin(UsersTags) \
        .outerjoin(Tag, Tag.id == UsersTags.tag_id) \
        .outerjoin(TagsCategories, Tag.id == TagsCategories.tag_id) \
        .outerjoin(TagCategory, TagCategory.id == TagsCategories.tag_category_id) \
        .filter(
            db.or_(
                TagCategory.id == main_category_id,  # Filter by 'main' category
                TagCategory.id.is_(None)  # Include users with no tags
            )
        ) \
        .order_by(User.hunt_years) \
        .all()

    team_users = defaultdict(list)
    unassigned_key = 'Ej tilldelade'

    for user in hunters:
        # Use first() to get the first UserHuntYear object, or None if there are none
        hunt_year = user.hunt_years.first()

        if hunt_year and hunt_year.hunt_team:
            team_name = hunt_year.hunt_team.name
        else:
            team_name = unassigned_key

        team_users[team_name].append(user)

    return render_template('admin/manage_huntteam.html.j2', users=users, teams=teams, years=years, team_users=team_users, tags=tags, form=form)


@admin.route("/add_hunt_team", methods=["POST"])
@auth_required
def add_hunt_team():
    form = EditUserForm()
    user_id = request.form.get('user_id')
    hunt_team_id = request.form.get('hunt_team_id')
    hunt_year_id = request.form.get('hunt_year_id')

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
        return jsonify({'status': 'success', 'message': 'User added to team successfully'})
    else:
        print(form.errors)
        return jsonify({'status': 'error', 'message': 'Invalid form data you punk'})
