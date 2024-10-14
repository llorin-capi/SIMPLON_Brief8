import requests

API_VERSION = 3
API_BASE_URL = f"https://api.jcdecaux.com/vls/v{API_VERSION}/"
DEFAULT_CONTRACT_CITY = "nancy"
API_KEY = "0268e4acb8b862e790cbd23dd89798630c94d0e6"


def build_api_url(contract_city, api_key):
    """
    :param contract_city: The name of the city where the contract is executed.
    :param api_key: The API key for authentication.
    :return: The complete URL for accessing the station information API for the specified city and API key.
    """
    return f"{API_BASE_URL}stations?contract={contract_city}&apiKey={api_key}"


def fetch_station_data(api_url):
    """
    :param api_url: The URL of the JCDecaux API endpoint to fetch station data from.
    :return: The JSON response from the JCDecaux API if the request is successful.
    :raises Exception: If the request to the JCDecaux API fails with a status code other than 200.
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
    :param station_json: JSON object containing station information
    :return: Dictionary with station details including number, name, latitude, longitude, status, capacity, available bikes, and available stands
    """
    return {
        "numero": station_json['number'],
        "nom": station_json['name'],
        "latitude": station_json['position']['latitude'],
        "longitude": station_json['position']['longitude'],
        "statut": station_json['status'],
        "capacite": station_json['mainStands']['capacity'],
        "dispo_velos": station_json['mainStands']['availabilities']['bikes'],
        "dispo_stands": station_json['mainStands']['availabilities']['stands'],
    }


def get_stations(contract_city=DEFAULT_CONTRACT_CITY, api_key=API_KEY):
    """
    :param contract_city: The city for which to retrieve the station information. Defaults to the value of DEFAULT_CONTRACT_CITY.
    :param api_key: The API key used for authenticating with the external service. Defaults to the value of API_KEY.
    :return: A list of station information, where each station's information is parsed from the JSON response.
    """
    api_url = build_api_url(contract_city, api_key)
    station_data = fetch_station_data(api_url)
    return [get_station_info(station_json) for station_json in station_data]
