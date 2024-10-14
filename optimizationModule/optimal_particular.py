import pandas as pd
import networkx as nx

def distribute_bikes(station_data_path, distance_data_path, max_bikes_per_transfer=10, max_iterations=100):
    """
    Distributes bikes among stations based on available bikes and transport routes.

    Parameters:
    ----------
    station_data_path : str
        Path to the CSV file containing bike station data with bike counts.
    distance_data_path : str
        Path to the CSV file containing distance and cost information between stations.
    max_bikes_per_transfer : int, optional
        Maximum number of bikes to transfer in one trip (default is 10).
    max_iterations : int, optional
        Maximum number of iterations for the bike distribution process (default is 100).

    Returns:
    ----------
    tuple
        Updated DataFrame with bike counts and DataFrame with routes of transferred bikes.
    """
    # Load bike station data with bike counts
    data = pd.read_csv(station_data_path)

    # Check for data loading error
    if data.empty:
        raise ValueError("Error: Station data not loaded.")

    # Load the distance and cost table
    distance_df = pd.read_csv(distance_data_path)

    # Check for distance table loading error
    if distance_df.empty:
        raise ValueError("Error: Distance table not loaded.")

    # Step 1: Create a graph for transport
    G = nx.Graph()

    # Add edges with cost weights
    for _, row in distance_df.iterrows():
        G.add_edge(row['Station_1'], row['Station_2'], weight=row['Cost_Euros'])

    total_cost = 0
    all_routes = []  # To store routes

    # Start distributing bikes
    iteration_count = 0  # Iteration counter
    while iteration_count < max_iterations:
        iteration_count += 1  # Increment iteration counter

        # Get the station with the maximum number of bikes
        station_with_max_bikes = data.loc[data['Bikes_Count'].idxmax()]
        station_number = station_with_max_bikes['Number']
        bikes_available = station_with_max_bikes['Bikes_Count']

        # Check if the station with the maximum number of bikes has any bikes available
        if bikes_available <= 0:
            print(f"There are no available bikes at station {station_number}.")
            break

        # Get possible destinations (all stations)
        destinations = data['Number'].values.tolist()

        # Move bikes
        bikes_moved_in_this_iteration = 0  # Counter for moved bikes

        for dest in destinations:
            if bikes_available <= 0:
                break

            # Check transport cost
            if G.has_edge(station_number, dest):
                transport_cost = G[station_number][dest]['weight']

                # Transfer a maximum of 'max_bikes_per_transfer' bikes
                transfer_bikes = min(bikes_available, max_bikes_per_transfer)

                # Update the number of bikes
                data.loc[data['Number'] == station_number, 'Bikes_Count'] -= transfer_bikes
                data.loc[data['Number'] == dest, 'Bikes_Count'] += transfer_bikes

                # Update total cost
                total_cost += transport_cost

                # Record the route
                all_routes.append({
                    'From': station_number,
                    'To': dest,
                    'Bikes_Moved': transfer_bikes,
                    'Cost': transport_cost
                })

                # Update available bikes
                bikes_available -= transfer_bikes
                bikes_moved_in_this_iteration += transfer_bikes

        # If no bikes were moved during the iteration, exit the loop
        if bikes_moved_in_this_iteration == 0:
            print("No bikes were moved during this iteration. Exiting.")
            break

    # Check if no transport was performed
    if not all_routes:
        print("No transports were performed.")
        return data, pd.DataFrame(all_routes)

    print(f"Total transport cost: {total_cost:.2f} euros")

    # Convert routes to DataFrame
    routes_df = pd.DataFrame(all_routes)

    return data, routes_df

# Example of using the function
station_data_path = "data/data_with_bikes.csv"
distance_data_path = "data/distance_cost_table.csv"
updated_data, routes = distribute_bikes(station_data_path, distance_data_path)

# Save results to CSV files
updated_data.to_csv("data/distributed_bikes.csv", index=False)
routes.to_csv("data/routes.csv", index=False)
print("Updated bike distribution data successfully saved to 'data/distributed_bikes.csv'.")
print("Transport routes saved to 'data/routes.csv'.")
