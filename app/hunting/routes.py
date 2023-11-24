from flask import Blueprint, render_template_string, render_template
from flask_security import login_required, roles_accepted
from app.hunting.models import HuntTeam, AnimalType, AnimalShot, AnimalQuota, UserTeamYear
from app.hunting.forms import RegisterShotMoose
from app.users.models import User, UsersTags
from app.tag.models import Tag
from app import db



hunting = Blueprint('hunting', __name__, template_folder='templates')

@hunting.route("/")
@login_required
@roles_accepted('admin', 'hunter')
def home():
    hunt_team = HuntTeam.query.all()
    for i in hunt_team:
        print(i)
    return render_template_string(f"{hunt_team[0].name}")


@hunting.route("/register/moose", methods=['GET', 'POST'])
def register_moose():
    tag_names = ['shooter', 'doghandler']
    form = RegisterShotMoose()
    moose_types = AnimalType.query.filter(AnimalType.group == 'moose')
    hunters = User.query.join(UsersTags).join(Tag).filter(Tag.name.in_(tag_names)).all()
    form.moose_type.choices = [(mt.id, mt.name) for mt in moose_types]
    form.hunter.choices = [(h.id, f'{h.first_name} {h.last_name}') for h in hunters]

    if form.validate_on_submit():
        def get_hunt_team_for_user_and_year(user_id, hunt_year_id):
            user_team_year = UserTeamYear.query.filter_by(
                user_id=user_id, 
                hunt_year_id=hunt_year_id
            ).first()

            return user_team_year.hunt_team_id if user_team_year else None

        def find_quota_id(hunt_year_id, hunt_team_id, animal_type_id):
            quota = AnimalQuota.query.filter_by(
                hunt_year_id=hunt_year_id,
                hunt_team_id=hunt_team_id,
                animal_type_id=animal_type_id
            ).first()

            if quota:
                return quota.id
            else:
                # Handle the case where no matching quota is found
                return None
        
        hunt_year_id = 1
        hunt_team_id = get_hunt_team_for_user_and_year(form.hunter.data, hunt_year_id)
        quota_id = find_quota_id(
            hunt_year_id,
            hunt_team_id,
            form.moose_type.data
        )

        animal_shot = AnimalShot(
            date_shot = form.date.data,
            weight = form.weight.data,
            age = form.age.data,
            user_id = form.hunter.data,
            quota_id = quota_id,
            gender = "male"
        )
        db.session.add(animal_shot)
        db.session.commit()
    else:
        print(form.errors)

    return render_template('register/moose.html.j2', form=form)