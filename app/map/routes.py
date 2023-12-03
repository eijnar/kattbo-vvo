from flask import Blueprint, render_template
from app import db
from folium import Map, Marker, Icon, LayerControl, FeatureGroup
from geoalchemy2.shape import to_shape
from folium.plugins import LocateControl, Fullscreen
from app.hunting.models import Stand, Area
from app.map.forms import AddGeopointForm
from app.map.models import PointOfIntrest
from sqlalchemy import func


map = Blueprint('map', __name__, template_folder='templates')


@map.route('/')
def map_index():
    return render_template('map/index.html.j2')


@map.route('/mapview')
def mapview():

    def create_map_new():
        # Initialize map
        m = Map(location=[60.833577, 14.197137], zoom_start=13)

        # Create a dictionary to hold FeatureGroups for each area
        area_groups = {}

        # Query the database
        stands = db.session.query(Stand, Area).join(Area).all()

        for stand, area in stands:
            point = to_shape(stand.geopoint)
            lat, lon = point.y, point.x

            # Check if this area's FeatureGroup already exists; if not, create it
            if area.name not in area_groups:
                area_groups[area.name] = FeatureGroup(name=area.name)
                area_groups[area.name].add_to(m)

            # Create marker
            marker = Marker([lat, lon], popup=f'Stand Number: {stand.number}')

            # Add marker to the respective area's FeatureGroup
            marker.add_to(area_groups[area.name])

        icon_mapping = {
            'landmark': 'info-sign',
            'saltstone': 'cloud',
            'gathering_place': 'info-sign',
            # Add more mappings for each category
        }
        color_mapping = {
            'landmark': 'red',
            'saltstone': 'green',
            'gathering_place': 'yellow',
        }

        # Create a dictionary for FeatureGroups for each category
        category_groups = {}

        # Query the PointOfInterest table
        points_of_interest = PointOfIntrest.query.all()

        for poi in points_of_interest:
            point = to_shape(poi.geopoint)
            lat, lon = point.y, point.x

            # Determine the icon for the category
            icon = icon_mapping.get(poi.category, 'question-sign')  # default icon if category not in mapping
            color = color_mapping.get(poi.category, 'gray')

            # Check if this category's FeatureGroup already exists; if not, create it
            if poi.category not in category_groups:
                category_groups[poi.category] = FeatureGroup(name=poi.category)
                category_groups[poi.category].add_to(m)

            # Create marker with the determined icon
            Marker(
                [lat, lon], 
                popup=f'{poi.name}: {poi.description}', 
                icon=Icon(color=color, icon=icon)
            ).add_to(category_groups[poi.category])

        # Add LayerControl
        LayerControl(collapsed=False).add_to(m)

        return m

    def create_map():

        m = Map(location=[60.833577, 14.197137], zoom_start=13)
        points = db.session.query(Stand.number, func.ST_AsText(Stand.geopoint).label('coords'))
        #stands = db.session.query(Stand.number, func.ST_AsText(Stand.geopoint).label('coords'))
        for point in points:
            try:
                # Parse the point coordinates
                coords = point.coords[6:-1].split()
                Marker([float(coords[1]), float(coords[0])], popup=point.number).add_to(m)
                print(point.number)
            except Exception as e:
                print(f"Error processing point {point.name}: {e}")

        LocateControl().add_to(m)
        Fullscreen().add_to(m)
        LayerControl(collapsed=False).add_to(m)
        return m
    
    folium_map = create_map_new()
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