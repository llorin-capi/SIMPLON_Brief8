import folium
import geopy
import certifi
import ssl
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, List

DEFAULT_COUNTRY = "France"


def setup_ssl_context() -> None:
    """
    Sets up the SSL context for geopy to use a default context with a specified certificate file.

    This function creates a default SSL context using certifi's CA bundle and assigns it to geopy's default SSL context.

    :return: None
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ssl_context


def fetch_gps_coordinates(city: str, country: str = DEFAULT_COUNTRY) -> Tuple[float, float]:
    """
    :param city: The name of the city for which GPS coordinates are to be fetched.
    :param country: The name of the country where the city is located. Defaults to DEFAULT_COUNTRY.
    :return: A tuple containing the latitude and longitude of the specified location.
    """
    setup_ssl_context()
    geolocator = Nominatim(user_agent="my_geocoder")
    location_str = f"{city}, {country}"
    location = geolocator.geocode(location_str)
    return location.latitude, location.longitude


def get_centered_map(latitude: float, longitude: float) -> folium.Map:
    """
    :param latitude: The latitude coordinate for the center of the map.
    :param longitude: The longitude coordinate for the center of the map.
    :return: A Folium Map object centered at the provided latitude and longitude coordinates.
    """
    map_center = [latitude, longitude]
    centered_map = folium.Map(location=map_center, zoom_start=14)
    return centered_map

def get_occupation_color(score: float) -> str :
    """
    :param score: A float representing the occupation score
    :return: A string representing the corresponding color based on the occupation score
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


def add_locations_to_map(map_object: folium.Map, locations: List[Dict[str, any]]) -> folium.Map:
    """
    :param map_object: The folium.Map object to which the locations will be added.
    :param locations: A list of dictionaries where each dictionary contains 'dispo_velos', 'capacite', 'latitude', 'longitude', and 'nom' keys representing the properties of each location.
    :return: The folium.Map object with the locations added.
    """
    for location in locations:
        occupation = location['dispo_velos'] / location['capacite']
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location["nom"],
            icon=folium.Icon(color=get_occupation_color(occupation))
        ).add_to(map_object)

    return map_object
