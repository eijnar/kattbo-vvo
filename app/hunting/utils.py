from app.hunting.models import HuntYear, UserTeamYear, AnimalQuota
from datetime import date
from sqlalchemy import and_

def get_hunt_years():
    # Current date
    today = date.today()

    # Query for the current hunt year
    current_hunt_year = HuntYear.query.filter(
        and_(HuntYear.start_date <= today, HuntYear.end_date >= today)
    ).first()

    # Initialize previous and next hunt year queries
    prev_hunt_year = next_hunt_year = None

    if current_hunt_year:
        # Query for the previous hunt year
        prev_hunt_year = HuntYear.query.filter(
            HuntYear.end_date < current_hunt_year.start_date
        ).order_by(HuntYear.end_date.desc()).first()

        # Query for the next hunt year
        next_hunt_year = HuntYear.query.filter(
            HuntYear.start_date > current_hunt_year.end_date
        ).order_by(HuntYear.start_date).first()

    return current_hunt_year, prev_hunt_year, next_hunt_year

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