from app.hunting.models import UserTeamYear, AnimalQuota

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