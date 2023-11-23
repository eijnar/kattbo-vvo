from flask import Blueprint, render_template
from app import db
from folium import Map, Marker, DivIcon, LayerControl, FeatureGroup
from folium.plugins import LocateControl, Fullscreen
from app.map.forms import AddGeopointForm
from app.map.models import PointOfIntrest
from sqlalchemy import func


map = Blueprint('map', __name__, template_folder='templates')


@map.route('/')
def map_index():
    return render_template('map/index.html.j2')


@map.route('/mapview')
def mapview():
    def create_map():

        m = Map(location=[60.833577, 14.197137], zoom_start=13)
        points = db.session.query(PointOfIntrest.name, func.ST_AsText(PointOfIntrest.geopoint).label('coords'))
        print(f"Number of points: {points.count()}")
        for point in points:
            try:
                # Parse the point coordinates
                coords = point.coords[6:-1].split()
                Marker([float(coords[1]), float(coords[0])], popup=point.name).add_to(m)
                print(point.name)
            except Exception as e:
                print(f"Error processing point {point.name}: {e}")

        LocateControl().add_to(m)
        Fullscreen().add_to(m)
        LayerControl(collapsed=False).add_to(m)
        return m
    
    folium_map = create_map()
    map_html = folium_map._repr_html_()

    return map_html

@map.route('/add_point', methods=['POST', 'GET'])
def add_geopoint():
    form = AddGeopointForm()
    if form.validate_on_submit():
        new_point_of_intrest = PointOfIntrest(
            name = form.name.data,
            geopoint = f'POINT({form.long.data} {form.lat.data})',
            description = form.description.data,
            category = form.category.data
        )
        db.session.add(new_point_of_intrest)
        db.session.commit()
        print(new_point_of_intrest)

    return render_template('map/new_point.html.j2', form=form)