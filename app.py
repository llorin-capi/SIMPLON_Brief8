from services import jcdecaux_services as jcds
from services import maps_services as maps

DEFAULT_COUNTRY = "France"


def fetch_and_map_stations():
    """
    Fetches station data, retrieves GPS coordinates for the default contract city,
    creates a centered map, and adds the station locations to the map.
    :return: None
    """
    stations = jcds.get_stations()
    latitude, longitude = fetch_coordinates_for_city(jcds.DEFAULT_CONTRACT_CITY)
    centered_map = create_centered_map(latitude, longitude)
    add_station_locations_to_map(centered_map, stations)


def fetch_coordinates_for_city(city):
    return maps.fetch_gps_coordinates(city, DEFAULT_COUNTRY)


def create_centered_map(latitude, longitude):
    return maps.get_centered_map(latitude, longitude)


def add_station_locations_to_map(map_object, stations):
    maps.add_locations_to_map(map_object, stations)


if __name__ == '__main__':
    fetch_and_map_stations()
