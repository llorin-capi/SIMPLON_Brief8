import requests
import re

API_VERSION = 3
API_BASE_URL = f"https://api.jcdecaux.com/vls/v{API_VERSION}/"
DEFAULT_CONTRACT_CITY = "nancy"
API_KEY = "0268e4acb8b862e790cbd23dd89798630c94d0e6"


def build_api_url(contract_city, api_key):
    """
    :param contract_city: The name of the city for which the API URL is being constructed.
    :param api_key: The API key for accessing the data.
    :return: Constructed API URL string.
    """
    return f"{API_BASE_URL}stations?contract={contract_city}&apiKey={api_key}"


def fetch_station_data(api_url):
    """
    :param api_url: The URL of the JCDecaux API endpoint to fetch station data from.
    :return: The response data from the JCDecaux API in JSON format.
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(
            f"Request to JCDecaux API failed: {api_url}",
            response.status_code,
            response.text
        )
    return response.json()


def get_station_info(station_json):
    """
    :param station_json: JSON data representing station information
    :type station_json: dict
    :return: A dictionary with parsed station information including number, name, coordinates, status, capacity, available bikes, and available stands
    :rtype: dict
    """
    return {
        "numero": station_json['number'],
        "nom": re.sub(r'[\d-]', '', station_json['name']).strip(),
        "latitude": station_json['position']['latitude'],
        "longitude": station_json['position']['longitude'],
        "statut": station_json['status'],
        "capacite": station_json['mainStands']['capacity'],
        "dispo_velos": station_json['mainStands']['availabilities']['bikes'],
        "dispo_stands": station_json['mainStands']['availabilities']['stands'],
    }


def get_stations(contract_city=DEFAULT_CONTRACT_CITY, api_key=API_KEY):
    """
    :param contract_city: The name of the city for which to retrieve the bike stations.
    :param api_key: The API key required for authenticating the request.
    :return: A list of station information for the specified city.
    """
    api_url = build_api_url(contract_city, api_key)
    station_data = fetch_station_data(api_url)
    return [get_station_info(station_json) for station_json in station_data]
