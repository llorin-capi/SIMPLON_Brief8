import pandas as pd
import numpy as np
import networkx as nx

def distribute_bikes(input_bike_file: str, input_distance_file: str, output_file: str, required_bikes: int = 10):
    """
    Distributes bikes from stations with the highest count to those with the least, minimizing transport costs.

    Parameters:
    - input_bike_file (str): The path to the CSV file containing bike data at each station.
    - input_distance_file (str): The path to the CSV file containing distance and cost information.
    - output_file (str): The path to the output CSV file where the updated bike distribution will be saved.
    - required_bikes (int): The minimum number of bikes each station should have. Default is 10.

    Returns:
    - None: Saves the updated DataFrame to a CSV file.
    """
    # Load bike data from the specified input CSV file
    data = pd.read_csv(input_bike_file)

    # Load distance and cost data from the specified input CSV file
    distance_df = pd.read_csv(input_distance_file)

    # Step 1: Find the station with the maximum number of bikes
    max_bikes_station = data.loc[data['Bikes_Count'].idxmax()]
    max_bikes_station_number = max_bikes_station['Number']
    max_bikes_count = max_bikes_station['Bikes_Count']

    print(f"The station with the maximum number of bikes: {max_bikes_station_number} ({max_bikes_count} bikes)")

    # Step 2: Determine the needs of other stations (e.g., minimum of 10 bikes at each station)
    data['Need'] = required_bikes - data['Bikes_Count']

    # Step 3: Move bikes at minimal cost
    # Create a graph for transportation
    G = nx.Graph()

    # Add edges with weights representing transportation costs
    for _, row in distance_df.iterrows():
        G.add_edge(row['Station_1'], row['Station_2'], weight=row['Cost_Euros'])

    total_cost = 0

    # Start distributing bikes
    while data['Need'].sum() > 0:  # While there are stations in need of bikes
        # Sort stations by number of bikes and transport cost
        needs = data[data['Need'] > 0].copy()
        if needs.empty:
            break

        # Get the station with the maximum number of bikes
        station_with_max_bikes = data.loc[data['Bikes_Count'].idxmax()]

        # Move bikes from the station with the maximum number of bikes
        station_number = station_with_max_bikes['Number']
        bikes_available = station_with_max_bikes['Bikes_Count']

        # Get possible destinations
        destinations = needs['Number'].values.tolist()

        for dest in destinations:
            if bikes_available <= 0:
                break

            # Check transportation cost
            if G.has_edge(station_number, dest):
                transport_cost = G[station_number][dest]['weight']
                
                # Determine how many bikes can be transferred
                transfer_bikes = min(bikes_available, required_bikes - data.loc[data['Number'] == dest, 'Bikes_Count'].values[0])

                # Update the number of bikes
                data.loc[data['Number'] == station_number, 'Bikes_Count'] -= transfer_bikes
                data.loc[data['Number'] == dest, 'Bikes_Count'] += transfer_bikes

                # Update needs
                data.loc[data['Number'] == dest, 'Need'] -= transfer_bikes

                # Update total transportation cost
                total_cost += transport_cost

                # Update available bikes
                bikes_available -= transfer_bikes

    print(f"Total transportation cost: {total_cost:.2f} euros")

    # Output updated station data
    print(data[['Number', 'Station', 'Bikes_Count', 'Need']])

    # Save the result to the specified output CSV file
    data.to_csv(output_file, index=False)
    print(f"Updated bike distribution successfully saved to '{output_file}'.")

# Example usage
distribute_bikes("data/data_with_bikes.csv", "data/distance_cost_table.csv", "data/distributed_bikes.csv")
