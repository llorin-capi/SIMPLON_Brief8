import folium
import geopy
import certifi
import ssl
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, List


def setup_ssl_context() -> None:
    """
    Sets up the SSL context for secure connections.

    This function initializes the default SSL context with the Certification Authority
    (CA) certificates provided by the certifi package. It then assigns this context
    to the default SSL context used by geopy geocoders.

    :return: None
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ssl_context


def fetch_gps_coordinates(city: str, country: str = "France") -> Tuple[float, float]:
    """
    :param city: Name of the city to fetch GPS coordinates for.
    :param country: Name of the country to fetch GPS coordinates for, default is "France".
    :return: A tuple containing the latitude and longitude of the specified location.
    """
    setup_ssl_context()
    geolocator = Nominatim(user_agent="my_geocoder")
    location_str = f"{city}, {country}"
    location = geolocator.geocode(location_str)
    return location.latitude, location.longitude


def get_centered_map(latitude: float, longitude: float) -> folium.Map:
    """
    :param latitude: Latitude coordinate for centering the map.
    :param longitude: Longitude coordinate for centering the map.
    :return: A Folium Map centered at the provided latitude and longitude.
    """
    map_center = [latitude, longitude]
    centered_map = folium.Map(location=map_center, zoom_start=14)
    return centered_map

def get_occupation_color(score):
    """
    :param score: A floating point number representing the score of the occupation.
    :return: A string representing the color associated with the given score. The color can be 'red' if the score is less than 0.15, 'orange' if the score is between 0.15 and 0.35, 'green' if the score is between 0.35 and 0.70, and 'purple' if the score is 0.70 or higher.
    """
    match score:
        case _ if score < 0.15:
            return 'red'
        case _ if 0.15 <= score < 0.35:
            return 'orange'
        case _ if 0.35 <= score < 0.70:
            return 'green'
        case _:
            return 'purple'


def add_locations_to_map(map_object: folium.Map, locations: List[Dict[str, any]]) -> None:
    """
    :param map_object: The Folium map object to which the locations will be added.
    :param locations: A list of dictionaries, each containing the keys 'dispo_velos', 'capacite', 'latitude', 'longitude', and 'nom'.
    :return: None
    """
    for location in locations:
        occupation = location['dispo_velos'] / location['capacite']
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location["nom"],
            icon=folium.Icon(color=get_occupation_color(occupation))
        ).add_to(map_object)
    map_object.save('map_locations.html')
