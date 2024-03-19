import re
import csv


# Change to the location of your testing sequence main file (seq.fna)
seq_filename = r"C:\...\testing_sequence\seq.fna"


# Opens seq.fna (test reads) and notes the starting location for each sequence number
def extract_numbers_from_file(filename):
    numbers = []
    rows = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file, start=1):
            matches = re.findall(r'>\s*(\d+)\s*', line)
            for match in matches:
                numbers.append(int(match))
                rows.append(i)
    return numbers, rows

# Takes the sequence number and its row in seq.fna and saves it to a CSV
def save_to_csv(numbers, rows, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Number', 'Row'])  # Write header
        for number, row in zip(numbers, rows):
            writer.writerow([number, row])

# Create list of sequence numbers and list of their respective row location
numbers, rows = extract_numbers_from_file(seq_filename)

# Create CSV of sequence numbers and list of their respective row location
csv_filename = "testnumberrows.csv"
save_to_csv(numbers, rows, csv_filename)