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

