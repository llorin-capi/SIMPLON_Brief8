import pandas as pd
import numpy as np

def generate_bike_data(input_file: str, output_file: str, max_bikes: int = 40, cost_per_bike: float = 2.0):
    """
    Generates random bike data for each station and calculates transport costs.

    Parameters:
    - input_file (str): The path to the input CSV file containing station data.
    - output_file (str): The path to the output CSV file where the updated data will be saved.
    - max_bikes (int): The maximum number of bikes a station can have. Default is 40.
    - cost_per_bike (float): The cost of transporting one bike. Default is 2.0 euros.

    Returns:
    - None: Saves the updated DataFrame to a CSV file.
    """
    # Load cleaned data from the input CSV file
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Set seed for reproducibility
    np.random.seed(42)

    # Generate a random number of bikes for each station between 0 and max_bikes
    data['Bikes_Count'] = np.random.randint(0, max_bikes + 1, size=len(data))

    # Define the involvement of the station (here it equals the number of bikes)
    data['Involvement'] = data['Bikes_Count']  # Maximum is max_bikes

    # Calculate the total transport cost for all bikes at each station
    data['Transport_Cost'] = data['Bikes_Count'] * cost_per_bike

    # Save the updated bike data to the output CSV file
    data.to_csv(output_file, index=False)
    print(f"Station data with bikes successfully saved to '{output_file}'.")

# Example usage
generate_bike_data("data/data_statique_clean.csv", "data/data_with_bikes.csv")
