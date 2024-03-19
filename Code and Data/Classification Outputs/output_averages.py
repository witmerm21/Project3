import csv
import os


# Change this to the directory of all the classification CSVs (output of NBC classify)
directory_path = r"C:\...\Output"


# Calculates the average of all read probabilities in a given CSV's third column
# Skips values larger than -5 (eg -3), some rows are just section headers yet still recieve a placeholder value
def calculate_average(file_path):
    total = 0
    count = 0
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and row[2]:  # Check if the row has at least 3 columns and the third column is not empty
                try:
                    value = float(row[2])
                    if value >= -5:  # Ignore values larger than -5
                        continue
                    total += value
                    count += 1
                except ValueError:
                    pass  # Ignore non-numeric values
    if count == 0:
        return None
    else:
        return total / count

# Iterates through every CSV file in a given directory, and calculates average for each using calculate_average()
# Creates a new CSV with each CSV name and its average
def process_files_in_directory(directory, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Average'])
        files = os.listdir(directory)
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory, file_name)
                average = calculate_average(file_path)
                if average is not None:
                    writer.writerow([file_name, average])
                else:
                    print(f"Ignoring file '{file_name}' as it has no valid values in the third column.")

# Create new CSV of all averages
output_file_path = "output_averages.csv"
process_files_in_directory(directory_path, output_file_path)
