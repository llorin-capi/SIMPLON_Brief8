import folium
import geopy
import certifi
import ssl
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, List


def setup_ssl_context() -> None:
    """
    Sets up the SSL context for geopy using certifi.
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ssl_context


def fetch_gps_coordinates(city: str, country: str = "France") -> Tuple[float, float]:
    """
    Fetches the GPS coordinates for a specified city and country.

    :param city: The name of the city to geocode.
    :param country: The country where the city is located. Defaults to "France".
    :return: A tuple containing the latitude and longitude of the specified city.
    """
    setup_ssl_context()
    geolocator = Nominatim(user_agent="my_geocoder")
    location_str = f"{city}, {country}"
    location = geolocator.geocode(location_str)
    return location.latitude, location.longitude


def get_centered_map(latitude: float, longitude: float) -> folium.Map:
    """
    Returns a folium Map object centered at the given latitude and longitude.

    :param latitude: Geographic coordinate that specifies the north-south position.
    :param longitude: Geographic coordinate that specifies the east-west position.
    :return: A folium Map object centered at the given latitude and longitude.
    """
    map_center = [latitude, longitude]
    centered_map = folium.Map(location=map_center, zoom_start=14)
    return centered_map


def add_locations_to_map(map_object: folium.Map, locations: List[Dict[str, any]]) -> None:
    """
    Adds location markers to an existing folium Map object.

    :param map_object: A folium Map object to which the locations will be added.
    :param locations: A list of location dictionaries containing latitude, longitude, and name.
    """
    for location in locations:
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location["nom"],
        ).add_to(map_object)
    map_object.save('map_locations.html')
