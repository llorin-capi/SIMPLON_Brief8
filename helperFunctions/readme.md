### Helper functions

## static_data.py - 
Purpose: The function reads a CSV file containing station data, processes the data to clean and extract relevant information, and saves the cleaned data to a new CSV file.

Steps Performed by the Function:
Read the CSV File:

The function takes two arguments: the path to the input CSV file and the path to the output CSV file.
It reads the CSV file into a Pandas DataFrame using pd.read_csv().
Display Original Data:

It prints the original DataFrame, specifically showing the Number, Name, Latitude, and Longitude columns for review.
Clean the Name Column:

A nested function named clean_name is defined. This function takes a string (the station name) and removes:
All digits (numbers).
All hyphens (-).
It then strips any leading or trailing whitespace from the cleaned string.
The cleaned names are stored in a new column called Station in the main DataFrame.
Create the CB Column:

A new column named CB is added to the DataFrame.
This column contains:
1 if the string (CB) is present in the Name column.
0 if the string (CB) is not present.
Remove the Name Column:

The original Name column is dropped from the DataFrame using data.drop(columns=['Name']).
Sort by Number:

The DataFrame is sorted by the Number column in ascending order using data.sort_values(by='Number').
Reset the Index:

The index of the DataFrame is reset using data.reset_index(drop=True, inplace=True), ensuring a clean, sequential index after sorting.
Display the Modified Data:

The function prints the modified DataFrame, showing the remaining columns: Number, Station, CB, Latitude, and Longitude.
Save Cleaned Data to a New CSV File:

Finally, the cleaned DataFrame is saved to a new CSV file specified by the output_file parameter using data.to_csv().
A confirmation message is printed to indicate the location of the saved cleaned data.
