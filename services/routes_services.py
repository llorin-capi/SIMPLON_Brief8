from services import jcdecaux_services as jcds
from services import maps_services as maps


def register_routes(app):
    """
    :param app: The application instance to which routes will be registered.
    :return: None

    """
    @app.route('/')
    def show_map_stations():
        city_stations = jcds.get_stations()
        city_centered_map = maps.get_centered_map(jcds.DEFAULT_CONTRACT_CITY)
        city_centered_map = maps.add_locations_to_map(city_centered_map, city_stations)

        return city_centered_map.get_root().render()