import pandas as pd
import requests
import re  # For using regular expressions

# API key, contract, and base URL
key = "e1d3b29a83a779db2a3c2d64d1d5a255c7560a27"
contract = "nancy"
api_base_url = "https://api.jcdecaux.com/vls/v3/"

# Function to clean the station name (remove digits, hyphens, "CB", and extra characters)
def clean_name(name):
    # Remove "CB", digits, hyphens, and extra spaces
    cleaned_name = re.sub(r'\bCB\b|[\d-]', '', name)  # Remove "CB", digits, and hyphens
    cleaned_name = re.sub(r'[\(\)\[\]\{\}]', '', cleaned_name)  # Remove parentheses and brackets
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()  # Remove extra spaces
    return cleaned_name

# Function to clean data
def clean_data(stations):
    cleaned_stations = []
    for station in stations:
        # Check for the presence of all necessary data
        if (station["Address"] and station["Latitude"] and station["Longitude"] and
            station["Station"] and station["Station_ID"] is not None and
            station["CurNumberOfBikes"] is not None and station["MaxNumberOfBikes"] is not None):
            
            # Check data validity (e.g., latitude and longitude must be numbers)
            try:
                station["Latitude"] = float(station["Latitude"])
                station["Longitude"] = float(station["Longitude"])
                station["CurNumberOfBikes"] = int(station["CurNumberOfBikes"])
                station["MaxNumberOfBikes"] = int(station["MaxNumberOfBikes"])

                # Clean station name and address
                station["Station"] = clean_name(station["Station"])
                station["Address"] = clean_name(station["Address"])

                cleaned_stations.append(station)  # Add the station if everything is okay
            except ValueError:
                # If data cannot be converted to the required types, ignore the station
                print(f"Error converting data for station {station['Station']}")
    return cleaned_stations

# Main function to retrieve data and clean it
def retrieve_stations():
    url = f"{api_base_url}stations?contract={contract}&apiKey={key}"
    response = requests.get(url)

    # Ensure correct encoding
    response.encoding = response.apparent_encoding

    if response.status_code == 200:
        stations = []
        for stat_station in response.json():
            # Create a structure according to the CSV file format
            station = {
                "Address": stat_station['name'],  # Assuming 'name' is the address
                "Latitude": stat_station['position']['latitude'],
                "Longitude": stat_station['position']['longitude'],
                "Station": stat_station['name'],  # Name of the station
                "CB": None,  # Placeholder for CB data (might consider gathering additional data later)
                "Station_ID": stat_station['number'],  # Station number as ID
                "CurNumberOfBikes": stat_station['mainStands']['availabilities']['bikes'],
                "MaxNumberOfBikes": stat_station['mainStands']['capacity']
            }
            stations.append(station)

        # Clean the data before creating DataFrame
        stations_cleaned = clean_data(stations)

        # Create DataFrame
        df_stations = pd.DataFrame(stations_cleaned, columns=[
            "Address", "Latitude", "Longitude", "Station", "CB", 
            "Station_ID", "CurNumberOfBikes", "MaxNumberOfBikes"
        ])
        
        # Save DataFrame to a CSV file
        df_stations.to_csv('./data/data_statique_clean01.csv', index=False)
        print("Data successfully saved to './data/data_statique_clean01.csv'.")

        return df_stations
    else:
        print("Error:", response.status_code)
        return None

# Example of using the function
df_stations = retrieve_stations()

# Output the first few rows for verification
if df_stations is not None:
    print(df_stations.head())
