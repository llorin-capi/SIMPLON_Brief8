import requests
from services import jcdecaux as jcd

# Fonction : récupération des contrats
def recup_contrats():
    url=jcd.api_base_url + "contracts?&apiKey=" + jcd.key
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        contrats=[]
        for contrat in response.json() :
            infos_contrat={
                "nom" : contrat['name'],
                "nom_commercial" : contrat['commercial_name']
            }
            contrats.append(infos_contrat)
        return contrats
    else:
        print("Erreur:", response.status_code)

# Fonction : récupération des données de toutes les stations vélos à l'instant t
def recup_stations():
    url=jcd.api_base_url + "stations?contract="+ jcd.contrat + "&apiKey=" + jcd.key
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        stations=[]
        for stat_station in response.json() :
            station={
            "numero" : stat_station['number'],
            "nom" : stat_station['name'],
            "latitude" : stat_station['position']['latitude'], #toujours float? besoin formattage?
            "longitude" : stat_station['position']['longitude'], #toujours float? besoin formattage?
            "statut" : stat_station['status'],
            "capacite" : stat_station['mainStands']['capacity'],
            "dispo_velos" : stat_station['mainStands']['availabilities']['bikes'],
            "dispo_stands" : stat_station['mainStands']['availabilities']['stands']
            }
            stations.append(station)
        return stations
    else:
        print("Erreur:", response.status_code)

