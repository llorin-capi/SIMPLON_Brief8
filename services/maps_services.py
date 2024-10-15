import folium
import geopy
import certifi
import ssl
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, List


def setup_ssl_context() -> None:
    """
    Sets up the SSL context required for secure communication by creating a default context
    using certificates from `certifi`. The context is then set as the default SSL context
    for `geopy.geocoders`.

    :return: None
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ssl_context


def fetch_gps_coordinates(city: str, country: str = "France") -> Tuple[float, float]:
    """
    :param city: Name of the city to fetch GPS coordinates for.
    :param country: Name of the country, defaults to "France".
    :return: Tuple containing the latitude and longitude of the city.
    """
    setup_ssl_context()
    geolocator = Nominatim(user_agent="my_geocoder")
    location_str = f"{city}, {country}"
    location = geolocator.geocode(location_str)
    return location.latitude, location.longitude


def get_centered_map(latitude: float, longitude: float) -> folium.Map:
    """
    :param latitude: Latitude coordinate around which the map should be centered.
    :param longitude: Longitude coordinate around which the map should be centered.
    :return: A Folium map object centered at the specified latitude and longitude.
    """
    map_center = [latitude, longitude]
    centered_map = folium.Map(location=map_center, zoom_start=14)
    return centered_map


def add_locations_to_map(map_object: folium.Map, locations: List[Dict[str, any]]) -> None:
    """
    :param map_object: The folium Map object to which the locations will be added.
    :param locations: A list of dictionaries, each containing the latitude, longitude, and name of a location to be added to the map.
    :return: None
    """
    for location in locations:
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location["nom"],
        ).add_to(map_object)
    map_object.save('map_locations.html')
