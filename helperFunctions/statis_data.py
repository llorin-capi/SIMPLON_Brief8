import pandas as pd
import re

def clean_name_and_extract_station(file_path, output_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(file_path, delimiter=',')  # Change delimiter if necessary (e.g., '\t' for tab)

    # Display the original DataFrame
    print("Original DataFrame:")
    print(data[['Number', 'Name', 'Latitude', 'Longitude']])  # Show 'Number', 'Name', 'Latitude', and 'Longitude'

    # Function to clean the 'Name' column by removing all numbers and hyphens
    def clean_name(name):
        # Remove digits and hyphens, and strip whitespace
        cleaned_name = re.sub(r'[\d-]', '', name).strip()
        return cleaned_name

    # Apply the cleaning function to the 'Name' column and create 'Station' column
    data['Station'] = data['Name'].apply(clean_name)

    # Add 'CB' column: 1 if '(CB)' is in 'Name', otherwise 0
    data['CB'] = data['Name'].apply(lambda name: 1 if '(CB)' in name else 0)

    # Drop the 'Name' column
    data = data.drop(columns=['Name'])

    # Sort by 'Number' column
    data = data.sort_values(by='Number')

    # Reset the index after sorting (optional)
    data.reset_index(drop=True, inplace=True)

    # Display the modified DataFrame
    print("\nModified DataFrame with 'Station' and 'CB' Columns (without 'Name') sorted by 'Number':")
    print(data[['Number', 'Station', 'CB', 'Latitude', 'Longitude']])  # Show all required columns

    # Save the cleaned DataFrame to a new CSV file
    data.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to {output_file}")

# Specify the file paths
input_file_path = "data/data_statique.csv"  # Update this with the correct path to your input file
output_file_path = "data/data_statique_clean.csv"  # Output file path

# Call the function
cleaned_data = clean_name_and_extract_station(input_file_path, output_file_path)


