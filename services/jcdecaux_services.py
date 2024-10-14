import requests

# URL BASE de l'API JC Decaux
api_base_url = "https://api.jcdecaux.com/vls/v1/"
# Ville contractante
contract_name = "nancy"
# Clé pour interrogation de l4API
api_key = "0268e4acb8b862e790cbd23dd89798630c94d0e6"
# URL complète pour récupération des données
api_stations_url = f"{api_base_url}stations?contract={contract_name}&apiKey={api_key}"

def get_stations():
    """
    Retrieves station data from the JCDecaux API.

    Makes a GET request to the specified API endpoint to obtain
    information about bike stations. If the request is successful,
    the station data is returned in JSON format. If the request fails,
    an exception is raised with details about the failure.

    :return: JSON response containing station data
    :rtype: dict
    :raises Exception: If the request to the JCDecaux API fails
    """
    response = requests.get(api_stations_url)
    if response.status_code != 200:
        raise Exception(
            "Request to JCDecaux API failed",
            response.status_code,
            response.text
        )
    return response.json()

def get_station_by_number(number):
