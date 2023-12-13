from flask import Blueprint, render_template
from app import db
from folium import Map, Marker, Icon, LayerControl, FeatureGroup, Figure
from geoalchemy2.shape import to_shape
from folium.plugins import LocateControl, Fullscreen
from app.models.hunting import Stand, Area
from app.blueprints.maps.forms import AddGeopointForm
from app.models.maps import PointOfIntrest


map = Blueprint('map', __name__, template_folder='templates')


@map.route('/')
def map_index():
    fullscreen=True
    return render_template('map/index.html.j2', fullscreen=fullscreen)


@map.route('/mapview')
def mapview():

    m = Map(location=[60.833577, 14.197137], zoom_start=13)
    f = Figure(height="100%", width="100%", ratio=None)
    f.add_child(m)
    # Create a dictionary to hold FeatureGroups for each area
    area_groups = {}

    # Query the database
    stands = db.session.query(Stand, Area).join(Area).all()

    for stand, area in stands:
        point = to_shape(stand.geopoint)
        lat, lon = point.y, point.x

        # Check if this area's FeatureGroup already exists; if not, create it
        if area.name not in area_groups:
            area_groups[area.name] = FeatureGroup(name=area.name, show=False)
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
        'landmark': 'lightred',
        'saltstone': 'white',
        'gathering_place': 'lightgreen',
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

    LocateControl().add_to(m)
    Fullscreen().add_to(m)
    LayerControl().add_to(m)

    return m.get_root().render()
    
    # folium_map = create_map_new()
    # map_html = folium_map._repr_html_()
    # map_html = folium_map[:1000] + '2' + folium_map[100:]

    # return map_html


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