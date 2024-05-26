import csv

# Input and output file paths
input_csv = 'stocks.csv'
output_csv = 'unique_symbols.csv'
output_py = 'symbols.py'

# Initialize a set to store unique symbols/names
unique_symbols = set()

# Read the input CSV file
with open(input_csv, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Product'] != 'Fixed Income':
            # ignore names like DVN
            # ignore symbols like DVN and VUX
            exclude_stocks = ['DVN', "BEE", "DM"]
            if row['Symbol/Name'] not in exclude_stocks:

                # map Symbol/Name to ticker, for example KNR goes to KNR.NE
                mapping_dict = {
                    "KNR": "KNR.NE",
                    "GXE": "GXE.TO",
                    "VUX": "VUX.TO",
                }
                mapping_name = row['Symbol/Name']
                # map Symbol/Name to ticker
                if mapping_name in mapping_dict:
                    # Perform the necessary operation when the key is found in the dictionary
                    ticker = mapping_dict[mapping_name]
                else:
                    ticker = mapping_name

                unique_symbols.add(mapping_name)

# Write unique symbols/names to output CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol/Name'])
    for symbol in sorted(unique_symbols):
        writer.writerow([symbol])

# Create a list of dictionaries for the unique symbols
symbols_list = [{'ticker': symbol, 'indicators': ['rsi', 'stoch']} for symbol in unique_symbols]

# Write the symbols_list to a Python file
with open(output_py, mode='w') as file:
    file.write("symbols = ")
    file.write(repr(symbols_list))

# Output the list of dictionaries
print(symbols_list)
