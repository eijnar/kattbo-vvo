from flask import Blueprint, render_template
import folium


map = Blueprint('map', __name__, template_folder='templates')


@map.route('/')
def map_index():
    return render_template('map/index.html.j2')


@map.route('/mapview')
def mapview():

    def create_map():
        m = folium.Map(location=[60.833577, 14.197137], zoom_start=13)
        return m
    
    folium_map = create_map()
    map_html = folium_map._repr_html_()

    return map_html