import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, LpInteger
import osmnx as ox

# Load data
@st.cache_data
def load_data():
    file_path = './data/data_statique_clean01.csv'
    data = pd.read_csv(file_path)
    return data

# Optimize bike redistribution
def optimize_bike_distribution(stations):
    num_stations = len(stations)
    
    # Optimization (similar to previous code)
    supply = stations['CurNumberOfBikes'].values
    mean_bikes = supply.mean()
    
    model = LpProblem("Bike_Redistribution", LpMinimize)
    
    # Variables for bike transfers
    transfer_vars = LpVariable.dicts("Transfer", ((i, j) for i in range(num_stations) for j in range(num_stations)),
                                      lowBound=0, cat=LpInteger)
    
    # Objective function - minimize transfers
    model += lpSum(transfer_vars[i, j] for i in range(num_stations) for j in range(num_stations) if i != j), "Minimize_Transfers"
    
    # Supply and demand constraints
    for i in range(num_stations):
        model += lpSum(transfer_vars[i, j] for j in range(num_stations) if i != j) <= supply[i], f"Supply_Constraint_{i}"
        model += lpSum(transfer_vars[j, i] for j in range(num_stations) if j != i) + supply[i] >= mean_bikes, f"Demand_Constraint_{i}"
    
    model.solve()
    
    results = []
    for i in range(num_stations):
        for j in range(num_stations):
            if (i != j) and transfer_vars[i, j].varValue is not None and transfer_vars[i, j].varValue > 0:
                results.append((i, j, int(transfer_vars[i, j].varValue)))
    
    return results

# Get routes via streets
def get_routes_via_streets(stations, transfers):
    # Load street graph using OSMnx
    G = ox.graph_from_place("Nancy, France", network_type='bike')
    
    routes = []
    for i, j, bikes in transfers:
        start_lat, start_lon = stations.iloc[i][['Latitude', 'Longitude']]
        end_lat, end_lon = stations.iloc[j][['Latitude', 'Longitude']]
        
        # Get nearest nodes in the graph for start and end points
        start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)
        
        # Find the shortest path along the streets
        try:
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            routes.append((route, bikes))
        except nx.NetworkXNoPath:
            # Skip nodes without a path
            pass
    
    return G, routes

# Plot map with routes
def plot_map_with_routes(stations, transfers, G, routes):
    map_center = [stations['Latitude'].mean(), stations['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=14)
    
    # Add station markers with bike information
    for i, station in stations.iterrows():
        # Determine marker color
        color = 'red' if any(j == i for _, j, _ in transfers) else 'blue'
        
        # Create marker with number of bikes
        marker = folium.Marker(
            location=[station['Latitude'], station['Longitude']],
            icon=folium.Icon(color=color),
            popup=f"{station['Station']}: {station['CurNumberOfBikes']} bikes"
        )
        marker.add_to(m)

    # Add bike transfer routes
    for (route, bikes) in routes:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        polyline = folium.PolyLine(
            route_coords, color='blue', weight=2, popup=f'Transfer: {bikes} bikes'
        ).add_to(m)

        # Create marker for the end of the route
        folium.Marker(
            location=route_coords[-1],
            popup=f"{bikes} bikes transferred",
            icon=folium.Icon(color='green')
        ).add_to(m)
    
    return m

# Streamlit interface
st.title('Bike Distribution Optimization with Street Routes')

# Sidebar with optimization results
with st.sidebar:
    st.header('Optimization Results')
    
    # Load data
    data = load_data()
    
    # Perform optimization
    transfers = optimize_bike_distribution(data)
    
    # Display optimization results
    st.write("Number of Stations: ", len(data))
    st.write("Transfers:")
    for i, j, bikes in transfers:
        st.write(f"From {data.iloc[i]['Station']} to {data.iloc[j]['Station']}: {bikes} bikes")
    
    # Button to rerun optimization
    if st.button('Rerun Optimization'):
        st.session_state.clear()  # Clear current state to refresh data

# Get routes via streets using OSMnx
G, routes = get_routes_via_streets(data, transfers)

# Display map in the central part
st.header('Bike Distribution Map with Street Routes')
bike_map = plot_map_with_routes(data, transfers, G, routes)

# Add a legend to the map
legend_html = """
<div style="position: fixed; 
     top: 10px; right: 10px; width: 150px; height: auto; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; padding: 10px;">
&nbsp; <b>Legend</b> <br>
&nbsp; <i style="color:red;">&#9679;</i>&nbsp; Bikes Delivered <br>
&nbsp; <i style="color:blue;">&#9679;</i>&nbsp; Station Not Receiving Bikes <br>
&nbsp; <i style="color:green;">&#9679;</i>&nbsp; Transfer Destination <br>
</div>
"""

# Add the legend to the map
bike_map.get_root().html.add_child(folium.Element(legend_html))

# Render the map
st_folium(bike_map, width=700, height=500)
