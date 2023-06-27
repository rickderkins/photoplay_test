import pandas as pd

# Load 'data.json' into a pandas DataFrame
data_file_path = 'material/data.json'
df = pd.read_json(data_file_path)
print(df['year'])

print(df)


# Request user inputs
year_input = int(input("Enter a year from the 'year' column: "))
string_input = input("Enter a string: ")

# Filter DataFrame based on the entered year_input
filtered_df = df[df['year'] == year_input]

# Check if any rows match the year_input
if filtered_df.empty:
    print("No matching rows found for the entered year.")
else:
    # Get the ner cell value for the first matching row
    ner_cell_value = filtered_df.iloc[0]['ner']

    # Flatten the list of lists
    flattened_list = [item for sublist in ner_cell_value for item in sublist]

    # Calculate the frequency of "{string_input}, 'person'" in the flattened list
    frequency = sum(1 for item in flattened_list if item == [string_input, 'PERSON'])

    # Print the frequency
    print("Frequency of '{}' in the 'ner' cell for the entered year: {}".format(string_input, frequency))
