from app.models.hunting import UserTeamYear, AnimalQuota

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