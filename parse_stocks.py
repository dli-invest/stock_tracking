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
            if 'DVN' not in row['Symbol/Name'] and 'VUX' not in row['Symbol/Name']:
                unique_symbols.add(row['Symbol/Name'])

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
