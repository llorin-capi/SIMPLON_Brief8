# Bike Distribution Optimization with Street Routes

This Streamlit application optimizes the redistribution of bikes among various stations in a city using the OSMnx library for routing and NetworkX for graph analysis. The app provides an interactive map that displays the bike stations, the number of bikes at each station, and the routes taken for bike transfers.

## Features

- Displays an initial map with bike stations.
- Optimizes the bike distribution using linear programming.
- Shows routes for bike transfers on the map.
- Interactive legend to explain color-coded markers.

## Requirements

Before running the app, ensure you have the following libraries installed:

- Streamlit
- Pandas
- Folium
- Streamlit-Folium
- NetworkX
- PuLP
- OSMnx

You can install the required packages using pip:

```bash
pip install streamlit pandas folium streamlit-folium networkx pulp osmnx
```
## Data
The application expects a CSV file named data_statique_clean01.csv in the data directory with the following columns:

* Station: The name of the bike station.
* Latitude: The latitude of the bike station.
* Longitude: The longitude of the bike station.
* CurNumberOfBikes: The current number of bikes at the station.
* Running the Application
* Clone the repository or download the files.

Navigate to the directory where the appBike.py file is located.

Run the Streamlit application using the following command:

```bash
streamlit run appBike.py
```
Open the provided local URL in your web browser to view the app.

Usage
Initial Map: The app will display the initial bike station map with markers showing the number of bikes at each station.
Optimize Bike Distribution: Click the "Optimize Bike Distribution" button to run the optimization algorithm. The sidebar will display the transfers needed, and the map will show the routes for bike redistribution.
Rerun Optimization: Use the "Rerun Optimization" button to refresh the data and run the optimization again.
Legend
The map includes a legend to indicate:

* Red Marker: Destination for bike deliveries.
* Blue Marker: Station not receiving bikes.
* Green Marker: Transfer destination.
