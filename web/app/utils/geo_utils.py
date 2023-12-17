from geoalchemy2 import functions as geo_func

def extract_lat_long(geopoint, session):
    """
    Extracts latitude and longitude from a WKBElement (geopoint).

    Args:
    - geopoint: A WKBElement representing a geographic point.
    - session: The SQLAlchemy session for executing the query.

    Returns:
    - A tuple (latitude, longitude).
    """
    latitude = session.scalar(geo_func.ST_Y(geopoint))
    longitude = session.scalar(geo_func.ST_X(geopoint))
    return latitude, longitude
