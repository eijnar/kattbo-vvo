from flask import Blueprint, render_template_string, render_template
from flask_security import login_required, roles_accepted
from models.hunting import HuntTeam, AnimalType, AnimalShot, AnimalQuota, UserTeamYear
from app.blueprints.hunting.forms import RegisterShotMoose
from app.blueprints.hunting.utils import get_hunt_team_for_user_and_year, find_quota_id
from models.users import User, UsersTags
from models.tag import Tag
from app.utils.hunt_year import HuntYearFinder
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
    hunt_year_finder = HuntYearFinder()
    current_hunt_year = hunt_year_finder.current

    if form.validate_on_submit():

        hunt_team_id = get_hunt_team_for_user_and_year(form.hunter.data, current_hunt_year.id)
        quota_id = find_quota_id(
            current_hunt_year.id,
            hunt_team_id,
            form.moose_type.data
        )
        
        if form.moose_type.data == 1: # Kalv
            animal_shot = AnimalShot(
                animal_type_id = form.moose_type.data,
                gender = form.gender.data,
                date_shot = form.date.data,
                weight = form.weight.data,
                age = "0.5",
                user_id = form.hunter.data,
                quota_id = quota_id,
            )

        elif form.moose_type.data == 2: # Oxe
            animal_shot = AnimalShot(
                animal_type_id = form.moose_type.data,
                date_shot = form.date.data,
                weight = form.weight.data,
                age = form.age.data,
                user_id = form.hunter.data,
                quota_id = quota_id,
                gender = "male",
                antler_type = form.antler_type.data,
                antlers = form.antlers.data
            )

        elif form.moose_type.data == 3: # Ko
            animal_shot = AnimalShot(
                animal_type_id = form.moose_type.data,
                date_shot = form.date.data,
                weight = form.weight.data,
                age = form.age.data,
                user_id = form.hunter.data,
                quota_id = quota_id,
                gender = "female",
                milk = form.milk.data
            )


        db.session.add(animal_shot)
        db.session.commit()
    else:
        print(form.errors)

    return render_template('register/register_moose.html.j2', form=form)

@hunting.route('/hunt_year/<int:hunt_year_id>/downed_animals')
def downed_animals(hunt_year_id):
    # Query to fetch downed animals and related user info
    downed_animals = AnimalShot.query \
        .join(User, AnimalShot.user_id == User.id) \
        .join(AnimalQuota, AnimalShot.quota_id == AnimalQuota.id) \
        .filter(AnimalQuota.hunt_year_id == hunt_year_id) \
        .all()

    return render_template('downed_animals.html.j2', downed_animals=downed_animals, hunt_year_id=hunt_year_id)