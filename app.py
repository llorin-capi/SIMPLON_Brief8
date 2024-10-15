from services import jcdecaux_services as jcds
from services import maps_services as maps
from flask import Flask, render_template
from services.routes_services import register_routes

DEFAULT_COUNTRY = "France"


def fetch_and_map_stations():
    """
    Fetches station data and maps their locations on a centered map.

    :return: None
    """
    stations = jcds.get_stations()
    latitude, longitude = fetch_coordinates_for_city(jcds.DEFAULT_CONTRACT_CITY)
    centered_map = create_centered_map(latitude, longitude)
    add_station_locations_to_map(centered_map, stations)


def fetch_coordinates_for_city(city):
    """
    :param city: The name of the city to fetch coordinates for.
    :return: GPS coordinates of the requested city.
    """
    return maps.fetch_gps_coordinates(city, DEFAULT_COUNTRY)


def create_centered_map(latitude, longitude):
    """
    :param latitude: The latitude coordinate for the center of the map.
    :param longitude: The longitude coordinate for the center of the map.
    :return: A map object centered at the specified latitude and longitude.
    """
    return maps.get_centered_map(latitude, longitude)


def add_station_locations_to_map(map_object, stations):
    """
    :param map_object: The map object to which station locations will be added.
    :type map_object: Map (object from a mapping library, e.g., folium.Map)
    :param stations: A list of station locations with their respective attributes.
    :type stations: list of dicts (each dict should include station location data such as latitude and longitude)
    :return: The updated map object with station locations added.
    :rtype: Map (same type as input map_object)
    """
    maps.add_locations_to_map(map_object, stations)

app = Flask(__name__)

register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)
