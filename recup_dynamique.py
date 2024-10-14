import requests

url = "https://api.jcdecaux.com/vls/v3/stations/8?contract=nancy&apiKey=e1d3b29a83a779db2a3c2d64d1d5a255c7560a27"
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
    print("Erreur:", response.status_code)
