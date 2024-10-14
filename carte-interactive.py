import osmnx as ox
import folium
import pandas as pd
import recup_dynamique as recup

# Création de la carte interactive avec Folium
map_center = [48.6921, 6.1847]  # coordonnées GPS de Nancy
m = folium.Map(location=map_center, zoom_start=14)

# Couleurs selon le taux d'occupation
def couleur_occupation(score):
    if score < 0.15:
        return 'red'
    elif 0.15 <= score < 0.35:
        return 'orange'
    elif 0.35 <= score < 0.70:
        return 'green'
    else :
        return 'purple'

# Création de la légende de la carte

# Récupération des données des stations
stations=recup.recup_stations()

# Ajout des stations à la carte
for station in stations :
    occupation=station['dispo_velos']/station['capacite']
    print(occupation)
    folium.Marker(
        location=[station["latitude"], station["longitude"]],
        popup=station["nom"],
        icon=folium.Icon(color=couleur_occupation(occupation))
    ).add_to(m)

# Sauvegarde de la carte
m.save('map_nancy.html')

