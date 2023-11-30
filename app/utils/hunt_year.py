from app.hunting.models import HuntYear
from sqlalchemy import and_
from datetime import date

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