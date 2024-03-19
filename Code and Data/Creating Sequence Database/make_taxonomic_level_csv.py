import pandas as pd
import csv


# Change to location of the output file from 'make_ncbi_csv.py'
file_path = r"C:\...\sequences.csv"


# Converts CSV file to list of lists
def read_csv_to_list(file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    # Convert the DataFrame to a list of lists
    data = df.values.tolist()
    return data

# Gets value of cell using row number and column header
def get_cell(csv_data, row_index, column_name, column_to_index):
    if row_index < len(csv_data) and column_name in column_to_index:
        col_index = column_to_index[column_name]
        if col_index < len(csv_data[row_index]):
            return csv_data[row_index][col_index]
    return None

# Create CSV file from n number of dictionaries
def write_dicts_to_csv(filename, *dicts):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Writing headers
        writer.writerow([
            'Domain', '#',
            'Kingdom', '#',
            'Phylum', '#',
            'Class', '#',
            'Order', '#',
            'Family', '#'
        ])
        # Writing rows
        dicts_len = []
        for d in dicts:
            dicts_len.extend([len(d)])
        dicts_max = max(dicts_len)
        for i in range(dicts_max):
            row = []
            for d in dicts:
                if i < len(d):
                    row.extend([list(d)[i], list(d.values())[i]])
                else:
                    row.extend(['', ''])
            writer.writerow(row)

# Import CSV file from make_ncbi_csv.py (sequences.csv)
csv_data = read_csv_to_list(file_path)

# Make dictionary that relates column headers to list number
column_to_index = {
    'folder': 0,
    'file': 1,
    'sequence': 2,
    'domain': 3,
    'kingdom': 4,
    'phylum': 5,
    'class': 6,
    'order': 7,
    'family': 8
}

# Create dictonaries for all unique taxonomic levels
# Each unique entry includes the number of occurances
csv_rows = len(csv_data)

domains_all = []
kingdoms_all = []
phylums_all = []
classes_all = []
orders_all = []
famlies_all = []
# Make a list of every entry for each taxonomic level
for i in range(1,csv_rows):
    domains_all.append(get_cell(csv_data, i, 'domain', column_to_index))
    kingdoms_all.append(get_cell(csv_data, i, 'kingdom', column_to_index))
    phylums_all.append(get_cell(csv_data, i, 'phylum', column_to_index))
    classes_all.append(get_cell(csv_data, i, 'order', column_to_index))
    orders_all.append(get_cell(csv_data, i, 'class', column_to_index))
    famlies_all.append(get_cell(csv_data, i, 'family', column_to_index))

# Count how many unique occurences there are for each taxonomic group per level
domains_unq = {}
for x in domains_all:
    if x not in domains_unq:
        domains_unq[x] = 0
    domains_unq[x] += 1

kingdoms_unq = {}
for x in kingdoms_all:
    if x not in kingdoms_unq:
        kingdoms_unq[x] = 0
    kingdoms_unq[x] += 1

phylums_unq = {}
for x in phylums_all:
    if x not in phylums_unq:
        phylums_unq[x] = 0
    phylums_unq[x] += 1

classes_unq = {}
for x in classes_all:
    if x not in classes_unq:
        classes_unq[x] = 0
    classes_unq[x] += 1

orders_unq = {}
for x in orders_all:
    if x not in orders_unq:
        orders_unq[x] = 0
    orders_unq[x] += 1

famlies_unq = {}
for x in famlies_all:
    if x not in famlies_unq:
        famlies_unq[x] = 0
    famlies_unq[x] += 1

# Create CSV file from the dictionaries
write_dicts_to_csv('unique_levels.csv', domains_unq, kingdoms_unq, 
    phylums_unq, classes_unq, orders_unq, famlies_unq)
