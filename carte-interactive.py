import folium
import pandas as pd
import geopy
import certifi
import ssl
from geopy.geocoders import Nominatim
from services import jcdecaux_services as jcds


# Étape 2 : Lire le fichier CSV
stations_df = pd.read_csv('C:/Users/Utilisateur/SIMPLON_Brief8/carte_interactive/nancy.csv')

# Vérifiez les colonnes et le contenu
print(stations_df)  # Affiche les premières lignes du DataFrame
print(stations_df.columns)  # Affiche les noms des colonnes

# Supprimer les espaces dans les noms des colonnes
stations_df.columns = stations_df.columns.str.strip()

# Étape 3 : Créer une liste de stations à partir du DataFrame
stations = stations_df.to_dict(orient='records')

# Étape 4 : Créer une carte interactive avec Folium
map_center = [48.6921, 6.1847]
m = folium.Map(location=map_center, zoom_start=14)

# Étape 5 : Ajouter les stations à la carte
for station in stations:
    folium.Marker(
        location=[station["Latitude"], station["Longitude"]],
        popup=station["Name"],
    ).add_to(m)

# Sauvegarder la carte
m.save('map_nancy.html')