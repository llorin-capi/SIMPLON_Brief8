import pandas as pd
import numpy as np
import networkx as nx
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, LpInteger

# Function to calculate the distance between two points using the Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

# Load the data
file_path = './data/data_statique_clean01.csv'
data = pd.read_csv(file_path)

# Prepare the stations data
stations = data[['Station', 'Latitude', 'Longitude', 'CurNumberOfBikes', 'MaxNumberOfBikes']]
num_stations = len(stations)

# Create a complete graph and calculate distances
G = nx.complete_graph(num_stations)

# Add nodes with bike information
for index, row in stations.iterrows():
    G.nodes[index]['cur_bikes'] = row['CurNumberOfBikes']
    G.nodes[index]['max_bikes'] = row['MaxNumberOfBikes']

# Calculate distances and add edges
for i in range(num_stations):
    for j in range(num_stations):
        if i != j:
            lat1, lon1 = stations.iloc[i][['Latitude', 'Longitude']]
            lat2, lon2 = stations.iloc[j][['Latitude', 'Longitude']]
            distance = haversine(lat1, lon1, lat2, lon2)
            G[i][j]['weight'] = distance  # Store the edge weight

# Define the supply and maximum bikes
supply = stations['CurNumberOfBikes'].values
max_bikes = stations['MaxNumberOfBikes'].values

# Calculate the average number of bikes across all stations
mean_bikes = np.mean(supply)

# Define the optimization problem
model = LpProblem("Bike_Redistribution", LpMinimize)

# Define integer variables for bike transfers
transfer_vars = LpVariable.dicts("Transfer", ((i, j) for i in range(num_stations) for j in range(num_stations)), 
                                              lowBound=0, cat=LpInteger)

# Objective function - minimize total bike transfers
model += lpSum(transfer_vars[i, j] for i in range(num_stations) for j in range(num_stations) if i != j), "Minimize_Transfers"

# Constraints for the number of bikes
for i in range(num_stations):
    # Supply constraint (cannot transfer more than currently available)
    model += lpSum(transfer_vars[i, j] for j in range(num_stations) if i != j) <= supply[i], f"Supply_Constraint_{i}"
    
    # Demand constraint (must receive enough to reach the average)
    model += lpSum(transfer_vars[j, i] for j in range(num_stations) if j != i) + supply[i] >= mean_bikes, f"Demand_Constraint_{i}"

# Solve the model
model.solve()

# Print the status of the solution
print("Status:", LpStatus[model.status])

# Output the results
if LpStatus[model.status] == 'Optimal':
    print("\nOptimized bike transfers:")
    for i in range(num_stations):
        for j in range(num_stations):
            if (i != j) and (transfer_vars[i, j].varValue is not None and transfer_vars[i, j].varValue > 0):
                print(f"Transfer {int(transfer_vars[i, j].varValue)} bikes from {stations.iloc[i]['Station']} to {stations.iloc[j]['Station']}")

    total_cost = model.objective.value()
    print("Total transportation cost: €", total_cost)
else:
    print("Optimization failed.")
