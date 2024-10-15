import folium
import osmnx as ox
import networkx as nx
from typing import Tuple, Dict, List

DEFAULT_COUNTRY = "France"
INITIAL_ZOOM_LEVEL = 14


def get_osmnx_graph(city_location: str):
    """
    :param city_location: The geographical location in the form of a string, representing the city or place for which the OSMnx graph is to be retrieved.
    :return: A graph object representing the street network of the specified city or place, which is obtained using OSMnx's graph_from_place function.
    """
    graph = ox.graph_from_place(city_location, network_type="drive")


    return graph









def get_city_center(edges) -> List[float]:
    """
    :param edges: A GeoDataFrame containing the geographical edge data.
    :return: A list containing the latitude and longitude of the centroid of the union of all edges.
    """
    return [edges.unary_union.centroid.y, edges.unary_union.centroid.x]


def create_folium_map(city_center: List[float]) -> folium.Map:
    """
    :param city_center: A list of two floats representing the latitude and longitude of the city center.
    :return: A Folium map instance centered at the given city coordinates with an initial zoom level.
    """
    return folium.Map(location=city_center, zoom_start=INITIAL_ZOOM_LEVEL)


def add_geojson_to_map(edges, map_object: folium.Map) -> None:
    """
    :param edges: A GeoJSON object or file path representing the geographic features to be added to the map.
    :param map_object: A folium.Map object to which the GeoJSON features will be added.
    :return: None
    """
    folium.GeoJson(edges).add_to(map_object)


def get_centered_map(city: str, country: str = DEFAULT_COUNTRY) -> folium.Map:
    """
    :param city: Name of the city for which the map is to be centered.
    :param country: Name of the country in which the city is located, defaulting to DEFAULT_COUNTRY.
    :return: A folium Map object centered on the given city.
    """
    city_location = f"{city}, {country}"
    city_graph = get_osmnx_graph(city_location)
    nodes, edges = ox.graph_to_gdfs(city_graph)

    city_center = get_city_center(edges)
    centered_map = create_folium_map(city_center)

    return centered_map


def get_score_color(score: float) -> str:
    """
    :param score: A floating-point number representing a score.
    :return: A string representing a color based on the score's value.
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
    :param map_object: The map object to which locations will be added
    :param locations: A list of dictionaries, each representing a location with latitude, longitude, name, dispo_velos, and capacite keys
    :return: The updated folium Map object with added location markers
    """
    for location in locations:
        availability = location['dispo_velos'] / location['capacite']
        folium.Marker(
            location=[location["latitude"], location["longitude"]],
            popup=location["nom"],
            icon=folium.Icon(color=get_score_color(availability))
        ).add_to(map_object)
    return map_object
