import requests
from services import jcdecaux as jcd

def recup_stats_station(num_station):
    url= jcd.api_base_url + "stations/" + str(num_station) +"?contract=" + jcd.contrat + "&apiKey=" + jcd.key
    response = requests.get(url)
    if response.status_code == 200: #Test de la réponse
        stat_station = response.json()
        station={
            "numero" : stat_station['number'],
            "nom" : stat_station['name'],
            "latitude" : stat_station['position']['latitude'],
            "longitude" : stat_station['position']['longitude'],
            "statut" : stat_station['status'],
            "capacite" : stat_station['mainStands']['capacity'],
            "dispo_velos" : stat_station['mainStands']['availabilities']['bikes'],
            "dispo_stands" : stat_station['mainStands']['availabilities']['stands']
        }
        print(station)
    else:
        print("Récup stats station :", num_station, "- Erreur:", response.status_code)

def recup_nums_station():
    url=jcd.api_base_url + "stations?contract="+ jcd.contrat + "&apiKey=" + jcd.key
    response = requests.get(url)
    if response.status_code == 200:
        stations=[]
        for stat_station in response.json() :
            station={
            "numero" : stat_station['number'],
            "nom" : stat_station['name'],
            "latitude" : stat_station['position']['latitude'],
            "longitude" : stat_station['position']['longitude'],
            "statut" : stat_station['status'],
            "capacite" : stat_station['mainStands']['capacity'],
            "dispo_velos" : stat_station['mainStands']['availabilities']['bikes'],
            "dispo_stands" : stat_station['mainStands']['availabilities']['stands']
            }
            stations.append(station)
        print(stations)
    else:
        print("Erreur:", response.status_code)

print(recup_nums_station())
